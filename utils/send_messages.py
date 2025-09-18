import asyncio
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from database.models_db import User
from keyboards.barista_keyboard import get_review_keyboard, show_review_message
from utils.get_user import get_users_from_db
from utils.logging_config import bot_logger
from dataclasses import dataclass


@dataclass
class SendMessage:
    """Класс для отправки уведомлений о новых отзывах"""
    user_role: str
    user: User
    bot: Bot
    review_id: Optional[int] = None
    text: Optional[str] = None
    file_id: Optional[str] = None

    async def send_message(self):
        """Отправляет уведомление баристам о новом отзыве"""
        try:
            baristas = await get_users_from_db(self.user_role)
            for barista in baristas:
                await asyncio.sleep(0.5)
                await self._send_notification(barista)
        except TelegramBadRequest or Exception as e:
            # если нет ни одного бариста, рассылка идет по админам
            bot_logger.exception(f"Ошибка при отправке уведомления: {e}")
            admins = await get_users_from_db("admin")
            for admin in admins:
                await asyncio.sleep(0.5)
                await self._send_notification(admin)

        # except Exception as e:
        #     bot_logger.exception(f"Ошибка при отправке уведомления: {e}")

    async def _send_notification(self, barista):
        bot_logger.info(f"Попытка отправки бариста {barista.get('id')}")

        message_text = f"🆘 Новый отзыв #{self.review_id}\n"\
                       f"От: @{self.user.username}\n" + (f"\n{self.text}" if self.text else "")

        if self.file_id:
            bot_logger.debug(f'Отправляю сообщение с фоткой')
            await self.bot.send_photo(chat_id=barista.get('telegram_id'),
                                      photo=self.file_id,
                                      caption=message_text,
                                      reply_markup=show_review_message(self.review_id))

        else:
            await self.bot.send_message(
                barista.get('telegram_id'), message_text, reply_markup=show_review_message(self.review_id))


@classmethod
class BotMessage:
    bot: Bot