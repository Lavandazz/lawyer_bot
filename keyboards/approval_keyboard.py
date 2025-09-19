from aiogram.utils.keyboard import InlineKeyboardBuilder


def yes_or_no_btn():
    kb = InlineKeyboardBuilder()
    kb.button(text='Да', callback_data='approve_yes')
    kb.button(text='Нет', callback_data='approve_no')
    kb.adjust(2)
    return kb.as_markup()

def show_review_message(req_id: int):
    """ Клавиатура для уведомления о новом отзыве """
    kb = InlineKeyboardBuilder()
    kb.button(text='Скрыть', callback_data=f"clear_{req_id}")
    return kb.as_markup()
