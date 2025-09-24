from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.logging_config import bot_logger


async def requests_menu_kb(requests):
    kb = InlineKeyboardBuilder()
    for request in requests:
        pass

    kb.adjust(2)

    return kb.as_markup()
