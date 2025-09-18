from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models_db import Game


def games_kb():
    """
    Меню игр
    :return:
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='Предстоящие игры', callback_data='show_upcoming_games')
    kb.button(text='Прошедшие игры', callback_data='show_passed_games')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


async def show_games_kb(games: List[Game]):
    """
    Отображение клавиатуры с играми
    :param games: Передаем список объектов игр
    :return: kb
    """
    kb = InlineKeyboardBuilder()
    if games:
        for game in games:
            kb.button(text=game.title, callback_data=f'game_{game.id}')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


def game_registration_kb(game_id, status=None):
    """
    Меню записи на игру
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardBuilder()
    if status == "new":
        kb.button(text='🎮 Записаться на игру', callback_data=f'register_for_game_{game_id}')
    kb.button(text='⬅️ Назад', callback_data='back')
    kb.adjust(2)  # Располагаем кнопки в один столбец
    return kb.as_markup()
