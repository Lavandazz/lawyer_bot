from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButtonRequestUser


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
    # kb = InlineKeyboardMarkup(inline_keyboard=[
    #     [
    #         InlineKeyboardButton(
    #             text="📱 Поделиться контактом",
    #             request_user=KeyboardButtonRequestUser(
    #                 request_id=1,  # Произвольный ID для идентификации запроса
    #                 user_is_bot=False,  # Запрашиваем пользователя, а не бота
    #                 user_is_premium=None  # Не важно, является ли пользователь премиум
    #             )
    #         )
    #     ]
    # ])
    return kb
