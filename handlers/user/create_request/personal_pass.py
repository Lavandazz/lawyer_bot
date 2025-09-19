from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.cancel_state_handler import cancel_state_handler
from keyboards.back_keyboard import back_button
from states.menu_states import CreateRequest
from utils.config import bot
from utils.logging_config import bot_logger


async def creating_request_pass(call: CallbackQuery, state: FSMContext):
    """
    Загрузка трудового договора
    :param call: pass
    :param state: wait_pass
    """
    await call.message.delete()
    data = await state.get_data()

    if not data.get("personal_pass"):
        await call.message.answer(
            text=f"📎 Прикрепите фото бейджа/пропуска используя скрепку ниже.\n"
                 f"Для отмены нажмите на кнопку 'Назад' или команду /cancel",
            reply_markup=back_button()
        )
    else:
        await call.message.answer(
            text=f"Вы уже прикрепляли скриншот\n",
            reply_markup=back_button()
        )
    await state.set_state(CreateRequest.wait_pass)
    await cancel_state_handler(user_id=call.from_user.id, bot=bot, state=state)


async def creating_request_pass_save(message: Message, state: FSMContext):
    """
    Получение скрина из ЛК.
    Ожидание фото бейджа
    """
    if not message.photo:
        await message.answer(text="Пожалуйста, прикрепите фото бейджа/пропуска.\n"
                                  "Формат PNG, JPEG.")
        return

    file_id = message.photo[-1].file_id
    await state.update_data(personal_pass=file_id)

    await message.answer(text=f"Фото получено.\n"
                              f"Загрузите оставшиеся документы",
                         reply_markup=back_button())

    bot_logger.debug(f'получен скрин лк: {message.photo}, file_id: {file_id}')
    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)
