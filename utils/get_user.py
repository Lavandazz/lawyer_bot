from functools import wraps

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from tortoise.exceptions import DoesNotExist

from database.models_db import User
from utils.logging_config import bot_logger


async def is_admin(user_id) -> bool:
    """ Проверка администратора """
    try:
        user = await User.get(telegram_id=user_id)
        return user.role in ['admin', 'barista']
    except DoesNotExist:
        return False


async def get_users_from_db(user_role) -> list[dict]:
    """
    Функция для отображения списка юзеров, отфильтрованных по ролям. Например, админы или бариста.
    :param user_role: admin, barista, user
    :return: list[dict]
    """
    users = await User.filter(role=user_role).values('id', 'username', 'telegram_id', 'role')
    return users


async def get_role_user(user_id: int) -> str | None:
    try:
        user = await User.get(telegram_id=user_id)  # telegram_id=484385628
        if user:
            bot_logger.debug(f'Возврат роли: {user_id}, {user.role}')
            return user.role
        else:
            bot_logger.debug(f'Юзер не зарегистрирован: {user_id}')
            return None

    except DoesNotExist:
        bot_logger.error(f'Ошибка, Юзер не зарегистрирован: {user_id}')
        return None


def role_required(*roles):  # передача ролей
    def decorator(func):  # обертка
        @wraps(func)  # сохраняет оригинальное имя и описание функции
        async def wrapper(event: Message | CallbackQuery, role: str, *args, **kwargs):  # передаем событие, роли
            if role not in roles:
                try:
                    await event.answer("У вас нет доступа к этой функции.")
                except TelegramBadRequest:
                    await event.message.answer("У вас нет доступа к этой функции.")
                return
            return await func(event, role=role, *args, **kwargs)
        return wrapper
    return decorator


def admin_only(func):
    return role_required("admin")(func)
