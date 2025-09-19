import os

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models_db import User
from handlers.cancel_state_handler import cancel_state_handler
from keyboards.back_keyboard import back_button
from states.menu_states import CreateRequest
from utils.config import bot, CLIENTS_DIR
from utils.logging_config import bot_logger


async def creating_request_surname(call: CallbackQuery, state: FSMContext):
    """
    Загрузка трудового договора
    :param call: pass
    :param state: wait_pass
    """
    await call.message.delete()
    data = await state.get_data()

    if not data.get("surname"):
        await call.message.answer(
            text=f"Введите фамилию.\n"
                 f"Изменить будет нельзя."
                 f"Необходимо для того, чтобы структурировать Ваши документы."
                 f"Для отмены нажмите на кнопку 'Назад' или команду /cancel",
            reply_markup=back_button()
        )
    else:
        await call.message.answer(
            text=f"*Вы уже ввели данные:*\n"
                 f"{data['surname']}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button()
        )
    await state.set_state(CreateRequest.wait_surname)


async def creating_request_surname_save(message: Message, state: FSMContext):
    """
    Сохранение фамилии пользователя в state и создание папки для документов
    """
    bot_logger.debug(f'введена фамилия {message.text}')

    if not message.text or len(message.text) < 2:
        await message.answer(text="Пожалуйста, введите фамилию.\n")
        return
    surname = message.text.title()
    # Сохраняем фамилию
    user = await User.get(telegram_id=message.from_user.id)
    user.second_name = surname
    await user.save()

    await state.update_data(surname=surname)

    await message.answer(text=f"Спасибо.\n"
                              f"Загрузите оставшиеся документы",
                         reply_markup=back_button())

    bot_logger.debug(f'фамилия введена')
    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


