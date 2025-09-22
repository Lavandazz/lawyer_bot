from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tortoise.exceptions import IntegrityError

from database.models_db import User
from keyboards.approval_keyboard import yes_or_no_btn
from keyboards.menu_keyboard import inline_menu_kb
from keyboards.register_keyboard import get_phone_keyboard
from utils.config import bot

from utils.logging_config import bot_logger


async def start_registration_user(chat_id):
    """Регистрация пользователя"""
    await bot.send_message(chat_id=chat_id,
        text=f"Для работы с ботом необходимо подтвердить номер телефона.\n"
             f"Пожалуйста, пришлите номер телефона.",
        reply_markup=get_phone_keyboard()
    )


async def process_contact(message: Message, state: FSMContext):
    """
    Обрабатывает принятый контакт
    """
    contact = message.contact
    phone_number = contact.phone_number
    await state.update_data(phone=phone_number)
    await message.answer(text=f"Это ваш номер телефона: {phone_number}?",
                         reply_markup=yes_or_no_btn()
                         )


async def approve_phone(call: CallbackQuery, state: FSMContext):
    """
    Подтверждение номера телефона.
    Зависит от колбека approve_yes/approve_no. Если yes, то переходит в режим сохранения данных.
    No - возвращает в главное меню.
    """
    approval = call.data.split("_")[1]  # approve_yes/approve_no

    if approval == "yes":
        data = await state.get_data()
        phone_number = data.get("phone").replace('7', '')
        bot_logger.debug(f"Получен номер телефона: {phone_number}"
                         f"approval = {approval}, call_data = {call.data}")
        await save_contact(
            username=call.from_user.username,
            telegram_id=call.from_user.id,
            first_name=call.from_user.first_name,
            second_name=call.from_user.last_name,
            phone=phone_number
        )
        await call.message.edit_text(
            text=f"Главное меню.\n\n"
                 f"Кнопка - *Начать запрос* - переводит бота в режим принятия документов.\n"
                 f"Пожалуйста, перед началом работы, ознакомьтесь с инструкцией по команде /help.\n\n"
                 f"Ниже Вы можете зайти в личный кабинет, где отображаются все Ваши запросы.",
            reply_markup=await inline_menu_kb(call.from_user.id),
            parse_mode='Markdown'
        )
    else:
        await call.message.edit_text(
            text=f"необходимо пройти регистрацию.",
        )
        return
    await state.clear()


async def save_contact(username, telegram_id, first_name, second_name, phone):
    try:
        await User.create(
            username=username,
            telegram_id=telegram_id,
            first_name=first_name,
            second_name=second_name,
            phone=phone,
            role="user")
        bot_logger.info(f"Новый пользователь сохранен")
    except IntegrityError as e:
        bot_logger.exception(f"Пользователь {telegram_id} уже есть в базе: {e}")
    except Exception as e:
        bot_logger.exception(f"Ошибка регистрации пользователя: {e}")
