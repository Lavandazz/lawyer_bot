from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models_db import User
from utils.config import SUPERADMIN
from utils.logging_config import bot_logger


def admin_kb():
    """ Кнопки в отделе администрирования """
    kb = InlineKeyboardBuilder()
    kb.button(text="Статистика",
              callback_data="statistic")
    kb.button(text="Заявки на расчет",
              callback_data="requests")
    if SUPERADMIN:
        kb.row(InlineKeyboardButton(text='Запуск парсинга', callback_data='start_parse'))
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))

    return kb.as_markup()


def admin_stat_kb():
    """Клавиатура для статистики"""
    kb = InlineKeyboardBuilder()
    kb.button(text='За день', callback_data='stat_day')
    kb.button(text='За период', callback_data='stat_all')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


async def requests_kb(requests):
    """Клавиатура, которая отображает все запросы от пользователей по фамилиям"""
    kb = InlineKeyboardBuilder()
    for request in requests:
        kb.button(text=f"{request.user_id.second_name}", callback_data=f'request{request.id}')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()

