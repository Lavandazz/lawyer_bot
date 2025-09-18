from aiogram import Bot
from aiogram.types import CallbackQuery
from pytz import timezone
from datetime import datetime, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.config import SUPERADMIN, bot
from utils.generator_horoscope import start_generate_all_horoscopes
from utils.logging_config import scheduler_logger
from utils.shedulers.cleane_base_scheduler import get_first_day_next_month


async def generate_call_horo(call: CallbackQuery):
    """
    Запуск шедулера для генерации гороскопов по нажатию кнопки Суперадмином
    :param call:
    :return: гороскоп
    """
    now_date = datetime.now().date()
    bot = call.bot
    await start_generate_all_horoscopes(bot, now_date)


async def generate_horo(bot: Bot):
    """ Вызов генерации гороскопа для шедулера"""
    now_date = datetime.now().date()
    print(f"Тип bot: {type(bot)}")
    await start_generate_all_horoscopes(bot, now_date)
    # await bot.send_message(chat_id=SUPERADMIN, text='Начал генерацию гороскопа в тестовом режиме')


async def scheduler_horoscope():
    """ Запуск шедулера """
    horo_timezone = timezone('Europe/Moscow')
    next_date = get_first_day_next_month()
    # next_date = date(year=2025, month=8, day=20)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(generate_horo,
                      trigger="date",
                      run_date=datetime(
                          year=next_date.year, month=next_date.month, day=1, hour=14, minute=42, second=0
                      ),
                      timezone=horo_timezone,
                      args=[bot])
    scheduler.start()
    scheduler_logger.info(f'Гороскопный шедулер запущен в {next_date}')