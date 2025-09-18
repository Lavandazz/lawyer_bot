# from aiogram import Bot
#
# from database.models_db import AdminPost
# from utils.config import CHANNEL
# from utils.logging_config import bot_logger
#
#
# async def publish_post_to_channel(bot: Bot, photo_id: str, text: str, post_id):
#     """ Публикация постов в канале """
#     try:
#         await bot.send_photo(chat_id=CHANNEL,
#                              photo=photo_id,
#                              caption=text)
#         await AdminPost.filter(id=post_id).update(status="published")  # изменяем поле status
#
#         bot_logger.info(f'Пост опубликован')
#     except Exception as e:
#         bot_logger.error(e)
#
#
# async def forward_review_to_channel(bot: Bot, from_chat_id: int, message_id: int):
#     """ Публикация отзыва клиента в канале """
#     try:
#         await bot.forward_message(chat_id=CHANNEL, from_chat_id=from_chat_id, message_id=message_id)
#         bot_logger.info(f'Отзыв переслан в канал')
#     except Exception as e:
#         bot_logger.exception(f'Ошибка пересылки отзыва: {e}')