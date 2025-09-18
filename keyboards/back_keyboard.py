from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_button():
    """ Кнопка назад """
    kb = InlineKeyboardBuilder()
    kb.button(text='⬅️ Назад', callback_data='back')
    kb.adjust(1)
    return kb.as_markup()


def farther_and_back_button():
    """ Кнопка вперед """
    kb = InlineKeyboardBuilder()
    kb.button(text='⬅️ Назад', callback_data='back')
    kb.button(text='➡️ Далее', callback_data='farther')
    kb.adjust(2)
    return kb.as_markup()
