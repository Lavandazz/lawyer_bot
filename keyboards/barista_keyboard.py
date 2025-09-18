from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models_db import Review, AdminPost
from utils.logging_config import bot_logger


""" Раздел, отвечающий за создание, отображение постов бариста """


def barista_menu_kb():
    """
    Клавиатура с кнопками Игры и Посты
    :return: kb
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Игры",
              callback_data="games")
    kb.button(text="Посты",
              callback_data="posts")
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


def barista_game_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить игру",
              callback_data="add_game"),
    kb.button(text="Удалить игру",
              callback_data="delete_game"),
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


def barista_kb():
    """ Кнопки в отделе администрирования """
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить пост",
              callback_data="add_post")
    kb.button(text="Посты бариста",
              callback_data="barista_posts"),
    kb.button(text="Отзывы пользователей",
              callback_data="moderate"),

    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


async def barista_posts_kb():
    """ Отображение постов бариста как кнопок """
    kb = InlineKeyboardBuilder()
    posts = await AdminPost.all()
    bot_logger.debug(f'Показываю кнопки с постами')
    # if not posts:
    #     kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))

    for post in posts:
        kb.button(text=post.text[:30]+'...', callback_data=f'post_{post.id}')

    kb.adjust(1)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


def get_post_keyboard():
    """ Кнопки для бариста """
    kb = InlineKeyboardBuilder()
    kb.button(text="Да, сгенерируй!", callback_data="generate_text")
    kb.button(text="Нет, введу вручную", callback_data="enter_text")

    kb.adjust(2)
    return kb.as_markup()


def edit_text_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Опубликовать", callback_data="save_post")
    kb.button(text="Отредактировать текст", callback_data="change_text")
    kb.adjust(2)
    return kb.as_markup()


""" Раздел работы бариста с отзывами клиентов """


async def review_kb():
    """ Кнопки с отзывами от клиентов """
    kb = InlineKeyboardBuilder()
    reviews = await Review.filter(approved=False).only("id", "created_at")
    if reviews:
        for review in reviews:
            date = review.created_at.strftime("%d.%m.%Y")
            kb.button(text=f'{date}',
                      callback_data=f'review_{review.id}')
        kb.adjust(3)

    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))  # добавляем отдельную кнопку в самый низ
    bot_logger.info('отправлена клавиатура с отзывами')
    return kb.as_markup()


def get_review_keyboard(review_id: int):
    """ Клавиатура для одобрения/отклонения отзыва """
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Одобрить", callback_data=f"approve_{review_id}")
    kb.button(text="❌ Отклонить", callback_data=f"reject_{review_id}")
    kb.button(text='⬅️ Назад', callback_data='back')
    kb.adjust(3)
    return kb.as_markup()


def show_review_message(review_id: int):
    """ Клавиатура для уведомления о новом отзыве """
    kb = InlineKeyboardBuilder()
    kb.button(text='Скрыть', callback_data=f"clear_{review_id}")
    return kb.as_markup()


