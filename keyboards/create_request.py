from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def file_for_record():
    """Клавиатура для статистики"""
    kb = InlineKeyboardBuilder()
    kb.button(text='Договор ГПХ/Трудовой', callback_data='contract')
    kb.button(text='Скрин ЛК ВБ Джоб', callback_data='acc_screenshot')
    kb.button(text='бейдж/пропуск', callback_data='pass')
    kb.button(text='2 НДФЛ/пропуск', callback_data='ndfl')
    kb.button(text='Выписка ИЛС', callback_data='extract')
    kb.button(text='Трудовая книжка', callback_data='record')
    kb.button(text='Добавить комментарий', callback_data='comment')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='Отправить юристу', callback_data='send'))
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()

