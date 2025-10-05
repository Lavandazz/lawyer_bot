from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.config import RequestStatus
from database.models_db import SalaryRequest
from handlers.admin.users_requests import show_requests
from handlers.back.back_handler import delete_messages
from handlers.message_texts import start_text
from keyboards.back_keyboard import back_button
from keyboards.menu_keyboard import inline_menu_kb
from services.requests import RequestService
from states.menu_states import ApproveState, AdminMenuState
from utils.config import bot
from utils.get_user import admin_only, get_user
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
    # status, user_telegram = await change_status_request(request_id=request_id, status=RequestStatus.APPROVED)
    change_status, telegram_id = await RequestService.change_status_request(
        request_id=request_id, status=RequestStatus.APPROVED
    )

    stat = await state.get_state()

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
        except Exception as e:
            bot_logger.exception(e)


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
    # await change_status_request(request_id=request_id, status=RequestStatus.REJECTED, comment=comment)

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
