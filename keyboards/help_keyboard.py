import logging

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def help_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Как пользоваться ботом", callback_data="how_use")
    kb.button(text="Как загружать документы", callback_data="how_upload")
    kb.button(text="Какие документы нужны", callback_data="what_upload")
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='❌ Скрыть вопросы', callback_data='hide_faq'))
    return kb.as_markup()


def help_docs_kb(kb_for_question):
    """ Кнопки с вопросами """
    kb = InlineKeyboardBuilder()

    for key, value in kb_for_question.items():
        kb.button(text=key, callback_data=value[0])

    kb.adjust(2)
    # Добавляем кнопку 'Скрыть'
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))

    return kb.as_markup()
