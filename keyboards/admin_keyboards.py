from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models_db import SalaryRequest
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


async def requests_kb(requests: List[SalaryRequest], role: str):
    """
    Принимаем объекты SalaryRequest из бд и делаем из них клавиатуру с кнопками вида Иванов.И.В.
    :param requests: список из объектов SalaryRequest
    :return: клавиатура по ФИО
    """
    kb = InlineKeyboardBuilder()
    for request in requests:
        # название кнопок берем из названия папок (contract - путь к папкам)
        btn = request.contract.split("\\")[1].replace("_", ".")
        if role == "admin":
            kb.button(text=f"{btn}", callback_data=f'admin_request_{request.id}')
        else:
            kb.button(text=f"{btn}", callback_data=f'user_request_{request.id}')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()

