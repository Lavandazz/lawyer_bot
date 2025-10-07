from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.config import RequestStatus

from handlers.back.back_handler import delete_messages
from handlers.message_texts import start_text
from keyboards.back_keyboard import back_button
from services.requests import RequestService
from states.menu_states import ApproveState
from utils.config import bot
from utils.get_user import admin_only
from utils.logging_config import bot_logger


@admin_only
async def approve_user_request(call: CallbackQuery, role: str, state: FSMContext):
    """
    Согласование заявки пользователя.
    request_id - получаем id из колбека
    Кнопка - Одобрить
    :param call: approve_{request_id}
    :param role:
    :param state:
    :return:
    """
    request_id = int(call.data.split('_')[2])

    change_status, telegram_id = await RequestService.change_status_request(
        request_id=request_id, status=RequestStatus.APPROVED
    )

    if change_status:
        try:
            await call.answer("Сохранено")
            # удаляем сообщения с фото и файлами
            await delete_messages('media_message_ids', call, state)

            await call.message.edit_text(text=start_text,
                                         reply_markup=back_button(),
                                         parse_mode='Markdown')

            await bot.send_message(chat_id=telegram_id,
                                   text="Ваша заявка рассмотрена и принята в работу.\n"
                                        "С вами свяжется юрист.")
            bot_logger.info(f"Согласование заявки {request_id}")

        except Exception as e:
            bot_logger.exception(f"Ошибка согласования заявки {request_id}: {e}")


@admin_only
async def comment_user_request(call: CallbackQuery, role: str, state: FSMContext):
    """
    Отклонение заявки пользователя.
    request_id - получаем id из колбека
    Кнопка - Отклонить
    :param call: approve_{request_id}
    :param role:
    :param state:
    :return:
    """
    request_id = int(call.data.split('_')[2])

    await delete_messages('media_message_ids', call, state)

    await call.message.edit_text(text="Введите причину отклонения заявки: ")

    await state.update_data(reject_id=request_id)  # ключ для поиска id заявки на удаление
    await state.set_state(ApproveState.reject_comment)


@admin_only
async def reject_user_request(message: Message, role: str, state: FSMContext):
    """
    Отклонение заявки пользователя.
    request_id - получаем id из колбека
    Кнопка - Отклонить
    :param call: approve_{request_id}
    :param role:
    :param state:
    :return:
    """
    data = await state.get_data()
    request_id = data.get('reject_id')
    comment = message.text
    change_status, telegram_id = await RequestService.change_status_request(
        request_id=request_id, status=RequestStatus.REJECTED, comment=comment
    )

    if not change_status:
        await message.answer(text="Произошла ошибка.",
                             reply_markup=back_button())
        bot_logger.warning(f"Ошибка в изменении статуса заявки {request_id}")
        return

    await bot.send_message(chat_id=telegram_id,
                           text=f"Ваша заявка отклонена юристом.\n"
                                f"*Комментарий:*\n\n"
                                f"{comment}",
                           parse_mode=ParseMode.MARKDOWN)

    await message.answer(text="Сообщение отправлено заявителю",
                         reply_markup=back_button())

    bot_logger.info(f"Отклонение заявки {request_id}")
