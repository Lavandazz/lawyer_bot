from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from utils.logging_config import bot_logger


async def set_commands(bot: Bot, user_id: int = None):
    """ Создание кнопок """
    commands = [
        BotCommand(command='start',
                   description='Запуск бота'),
        BotCommand(command='help',
                   description='Помощь')
    ]


    # Устанавливаем команды по умолчанию
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    bot_logger.info('Установил команды')
