import asyncio
from aiogram import Bot
from aiogram.types import Message
from datetime import timezone
from tortoise.exceptions import IntegrityError

from database.models_db import User
from handlers.user.registeration import start_registration_user
from keyboards.menu_keyboard import inline_menu_kb

from utils.config import SUPERADMIN, TEL
from utils.generator_text import generate_day_or_night
from utils.logging_config import bot_logger


async def on_start(bot: Bot):
    """ Отправка сообщения о старте супер-админу """
    await bot.send_message(chat_id=SUPERADMIN, text='Я запустил lawyerBot, /start')


async def seed_admin():
    """
    При старте приложения, будет создан супер-админ
    """
    bot_logger.info('Проверка: seed_admin вызвана')
    try:
        admin = await User.filter(role='admin').exists()
        if not admin:
            await User.create(
                username="Админ",
                telegram_id=SUPERADMIN,
                first_name="Марина",
                second_name="Овс",
                phone=TEL,
                role="admin"
            )
            bot_logger.info('Администратор зарегистрирован')

    except IntegrityError as e:
        bot_logger.info("Админ уже существует, пропускаем создание")

    except Exception as e:
        bot_logger.exception(f'Ошибка при создании админа {e}')


async def get_start(message: Message, bot: Bot, new_user: bool):
    """
    Хендлер команды /start.

    Действия:
    1. Если new_user == True — отправляет уведомление супер-админу о регистрации нового пользователя.
    2. Отправляет приветственное сообщение пользователю с учетом времени суток.
    3. Показывает главное меню и запускает стартовую логику приложения.
    """
    time_message = message.date
    # Преобразуем часовой пояс (+3 часа для Москвы)
    local_time = time_message.replace(tzinfo=timezone.utc).astimezone(tz=None)  # определяет локальный пояс
    try:

        if new_user:
            # Отправляем клавиатуру для подтверждения номера телефона
            await bot.send_message(chat_id=message.from_user.id,
                                   text="С ботом могут работать только зарегистрированные пользователи.\n"
                                   "Пожалуйста, пройдите регистрацию."
                                   )
            await asyncio.sleep(3)
            await start_registration_user(message.from_user.id)

            await bot.send_message(chat_id=SUPERADMIN, text=f'Зарегистрирован новый пользователь {message.from_user.id}')

        else:
            await bot.send_message(message.from_user.id,
                                   f"{generate_day_or_night(local_time.hour)}\n\n"
                                        f"Главное меню.\n\n"
                                        f"Кнопка - *Начать запрос* - переводит бота в режим принятия документов.\n"
                                        f"Пожалуйста, перед началом работы, ознакомьтесь с инструкцией для работы с ботом "
                                        f"по команде /help.\n\n"
                                        f"*Мои запросы* - Ваш личный кабинет, где отображаются все Ваши запросы.",
                                   reply_markup=await inline_menu_kb(message.from_user.id),
                                   parse_mode='Markdown')
            # await start_registration_user(message)

    except Exception as e:
        bot_logger.exception(f'Ошибка при создании админа {e}')

