from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.get_user import admin_only


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


def approve_request_kb(request_id: int, user_id: int):
    """ Клавиатура для одобрения/отклонения отзыва """
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Одобрить", callback_data=f"approve_{request_id}")
    kb.button(text="❌ Отклонить", callback_data=f"reject_{request_id}")
    kb.button(text="📞 Связаться", callback_data=f"contact_{user_id}")
    kb.adjust(3)
    return kb.as_markup()
