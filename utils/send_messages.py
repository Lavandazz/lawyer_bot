import asyncio
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from database.models_db import User
from keyboards.approval_keyboard import show_review_message
from utils.get_user import get_users_from_db
from utils.logging_config import bot_logger
from dataclasses import dataclass


@dataclass
class SendMessage:
    """Класс для отправки уведомлений о новых отзывах"""
    user_role: str
    user: User
    bot: Bot
    salary_request: Optional[int] = None
    text: Optional[str] = None
    file_id: Optional[str] = None

    async def send_message(self):
        """Отправляет уведомление админам о новой заявке"""
        try:
            admins = await get_users_from_db(self.user_role)
            for admin in admins:
                await asyncio.sleep(0.5)
                await self._send_notification(admin)
        except TelegramBadRequest or Exception as e:

            bot_logger.exception(f"Ошибка при отправке уведомления: {e}")

    async def _send_notification(self, admin):
        bot_logger.info(f"Попытка отправки админу {admin.get('id')}")

        message_text = f"📝 Новая заявка #{self.salary_request}\n"\
                       f"От: @{self.user.username}\n" + f"\n{self.text if self.text != 'pass' else ''}"

        await self.bot.send_message(
            admin.get('telegram_id'), message_text, reply_markup=show_review_message(self.salary_request))
