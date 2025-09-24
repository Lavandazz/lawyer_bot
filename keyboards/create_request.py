from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.save_docs import get_docs_from_state, expected_docs


#
# def file_for_record():
#     """Клавиатура для статистики"""
#     kb = InlineKeyboardBuilder()
#     kb.button(text='Договор ГПХ/Трудовой', callback_data='contract')
#     kb.button(text='Скрин ЛК ВБ Джоб', callback_data='acc_screenshot')
#     kb.button(text='бейдж/пропуск', callback_data='pass')
#     kb.button(text='2 НДФЛ', callback_data='ndfl')
#     kb.button(text='Выписка ИЛС', callback_data='extract')
#     kb.button(text='Электронная трудовая книжка', callback_data='record_book')
#     kb.button(text='Добавить комментарий', callback_data='comment')
#     kb.adjust(2)
#     kb.row(InlineKeyboardButton(text='Отправить юристу', callback_data='send'))
#     kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
#     return kb.as_markup()


async def file_for_record(state):
    """
    Клавиатура для отображения необходимых документов.
    Сначала видны все документы. По мере наполнения словаря result из функции get_docs_from_state,
    убывает список missing_docs, на основании значений которого строится клавиатура.
    Т.к. сначала missing_docs полный, то отображаются все документы.
    :param state:
    :return:
    """
    docs_data = await get_docs_from_state(state)

    missing_docs = docs_data['missing']
    kb = InlineKeyboardBuilder()
    for call, name in expected_docs.items():
        for doc in missing_docs:
            if doc in name:
                kb.button(text=name, callback_data=call)
    kb.button(text='Добавить комментарий', callback_data='comment')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='Отправить юристу', callback_data='send'))
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()
