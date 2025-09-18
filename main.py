import asyncio
from handlers.user.commands import set_commands
from handlers.dispatcher import setup_dispatcher
from handlers.user.start_handlers import seed_admin
from utils.config import dp, bot
from database.create_db import init_db, close_db
from utils.logging_config import bot_logger


async def start_bot(user_id: int = None):
    """ Запуск бота, при неудаче бот закроется """
    await set_commands(bot, user_id)
    # Регистрация хэндлеров
    setup_dispatcher(dp)

    # asyncio.create_task(scheduler_horoscope())
    # asyncio.create_task(scheduler_clean_horoscope(bot))
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        bot_logger.warning('Бот закрыт')
        await bot.close()


async def main():
    # Подключаем БД ОДИН РАЗ
    await init_db()
    # запись админа в бд
    await seed_admin()

    try:
        await start_bot()
    finally:
        await close_db()  # Закроем БД после завершения всех задач



if __name__ == '__main__':
    try:
        asyncio.run(main())
        bot_logger.info('>>> Бот запускается — main.py загружен!')
    except KeyboardInterrupt:
        bot_logger.warning('Помощник завершены')
