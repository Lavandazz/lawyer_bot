from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.get_user import get_role_user
from utils.logging_config import bot_logger


async def inline_menu_kb(user_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='Начать запрос', callback_data='start_request')
    kb.button(text='Мои запросы', callback_data='my_requests')
    kb.adjust(2)

    role = await get_role_user(user_id)  # получаем роль юзера
    bot_logger.debug(f'Передаю inline_menu_kb. Роль юзера: {role}')

    if role == 'admin':
        kb.row(InlineKeyboardButton(text='Админ-панель', callback_data='admin_panel'))

    return kb.as_markup()
