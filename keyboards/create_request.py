from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.config import EXPECTED_DOCS
from utils.save_docs import get_docs_from_state


async def file_for_record(state):
    """
    Клавиатура для отображения необходимых документов.
    Сначала видны все документы. По мере наполнения словаря result из функции get_docs_from_state,
    убывает список missing_docs, на основании значений которого строится клавиатура.
    Т.к. сначала missing_docs полный, то отображаются все документы.
    :param state: для получения state.data
    :return:
    """
    docs_data = await get_docs_from_state(state)

    missing_docs = docs_data['missing']
    kb = InlineKeyboardBuilder()
    for call, name in EXPECTED_DOCS.items():
        for doc in missing_docs:
            if doc in name:
                kb.button(text=name, callback_data=call)
    kb.button(text='Добавить комментарий', callback_data='comment')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='Отправить юристу', callback_data='send'))
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()
