from aiogram.utils.keyboard import InlineKeyboardBuilder


def yes_or_no_btn():
    kb = InlineKeyboardBuilder()
    kb.button(text='Да', callback_data='approve_yes')
    kb.button(text='Нет', callback_data='approve_no')
    kb.adjust(2)
    return kb.as_markup()