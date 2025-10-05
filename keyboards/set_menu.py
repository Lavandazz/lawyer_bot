from aiogram.types import BotCommand, BotCommandScopeDefault

from services.lexicon import LEXICON_COMMANDS
from utils.config import bot
from utils.logging_config import bot_logger


async def set_main_menu(user_id: int = None):
    """
    Команды start и help
    :param bot:
    :param user_id:
    :return:
    """

    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS.items()
    ]

    # Устанавливаем команды по умолчанию
    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeDefault())
    bot_logger.info('Установил команды')
