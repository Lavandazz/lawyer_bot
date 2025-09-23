import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tortoise.exceptions import IntegrityError

from database.models_db import User
from keyboards.approval_keyboard import yes_or_no_btn
from keyboards.back_keyboard import back_button
from keyboards.menu_keyboard import inline_menu_kb
from keyboards.register_keyboard import get_phone_keyboard
from states.menu_states import UserState
from utils.config import bot, SUPERADMIN

from utils.logging_config import bot_logger


async def start_registration_user(chat_id, state: FSMContext):
    """Регистрация пользователя"""
    await bot.send_message(chat_id=chat_id,
                           text=f"Для работы с ботом необходимо подтвердить номер телефона и ввести ФИО.\n"
                                f"Пожалуйста, напишите полностью Фамилию, Имя, Отчество.\n",
                           reply_markup=back_button()
                           )
    await state.set_state(UserState.register)


async def start_registration_user_name(message: Message, state: FSMContext):
    """Регистрация пользователя"""
    await state.update_data(fio=message.text)
    if not message.text or not len(message.text.split()) == 3:
        await message.answer(text="Введите ФИО полностью")
        return

    await message.answer(text=f"Отлично.\n"
                              f"Пришлите номер телефона",
                         reply_markup=get_phone_keyboard()
                         )
    await state.set_state(UserState.phone)


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
        fio_string = data.get("fio")
        phone_number = data.get("phone").replace('7', '')
        fio = split_fio(fio_string)

        # Сохраняем данные
        await save_contact(
            username=call.from_user.username,
            telegram_id=call.from_user.id,
            second_name=fio[0],
            first_name=fio[1],
            patronymic=fio[2],
            phone=phone_number
        )

        await bot.send_message(chat_id=SUPERADMIN, text=f'Зарегистрирован новый пользователь {call.from_user.id}')

        # Убираем Reply-клавиатуру отправкой нового сообщения
        mess = await bot.send_message(
            chat_id=call.from_user.id,
            text="Спасибо за регистрацию.",
            reply_markup=types.ReplyKeyboardRemove()
        )

        # Удаляем сообщение от бота о регистрацие (опционально)
        await asyncio.sleep(1)
        await bot.delete_message(chat_id=call.from_user.id, message_id=mess.message_id)

        # 4. Редактируем original сообщение
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
            text="Необходимо пройти регистрацию.",
        )
        return

    await state.clear()


def split_fio(full_fio:str):
    fio = full_fio.split()
    second_name = fio[0].title()
    name = fio[1].title()
    patronymic = fio[2].title()
    return second_name, name, patronymic


async def save_contact(username, telegram_id, second_name, first_name, patronymic, phone):
    try:
        await User.create(
            username=username,
            telegram_id=telegram_id,
            second_name=second_name,
            first_name=first_name,
            patronymic=patronymic,
            phone=phone,
            role="user")
        bot_logger.info(f"Новый пользователь сохранен")
    except IntegrityError as e:
        bot_logger.exception(f"Пользователь {telegram_id} уже есть в базе: {e}")
    except Exception as e:
        bot_logger.exception(f"Ошибка регистрации пользователя: {e}")
