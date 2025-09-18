from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_phone_keyboard():
    """
    Кнопка для  отправления телефона
    :return: KeyboardButton
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             one_time_keyboard=True,
                             selective=True,
                             keyboard=[
                                 [KeyboardButton(text="Отправить номер телефона",
                                  request_contact=True)]
                             ]
                             )
    return kb
