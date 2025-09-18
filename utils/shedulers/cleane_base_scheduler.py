from utils.config import admin_id

from aiogram import Bot
from aiogram.types import CallbackQuery
from pytz import timezone
from datetime import datetime, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models_db import Horoscope
from utils.logging_config import scheduler_logger


def get_first_day_next_month() -> date:
    """
    Вычисление первого дня следующего месяца для очистки базы от устаревших гороскопов
    :return: next_month - первый день следующего месяца
    """
    today = datetime.now().date()
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    return next_month
    # return datetime(2025, 6, 3).date()


async def horo_to_clean(bot: Bot):
    """
    Получение данных для удаления.
    Если дата гороскопа предшествует текущей дате, то строка попадает под удаление

    """
    current_date = datetime.now().date()
    # находим все даты меньше вчерашней и удаляем их
    try:
        old_horoscopes = await Horoscope.filter(date__lt=current_date).count()

        await bot.send_message(chat_id=admin_id, text=f'Очистка дат гороскопа: удалено {old_horoscopes} строк гороскопа')
        # await call.message.answer(text=f'удалено {old_horoscopes} трок гороскопа')
    except Exception as e:
        await bot.send_message(chat_id=admin_id, text=f'Очистка дат гороскопа не была проведена: {e}')
        scheduler_logger.warning(f'Ошибка при очистке дат гороскопа {datetime.now()}, {e}')


async def scheduler_clean_horoscope(bot: Bot):
    """
    Шедулер для очистки бд от устаревших гороскопов.
    Шедулер запускается на основании вычисленной даты next_month
    и запускается автоматически в первый день месяца в 15 часов 35 минут.

    """
    next_month = get_first_day_next_month()
    horo_timezone = timezone('Europe/Moscow')
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(horo_to_clean, "cron", hour=13, minute=53, timezone=horo_timezone, args=[bot])
    scheduler.add_job(horo_to_clean, "date",
                      run_date=datetime(year=next_month.year, month=next_month.month, day=1, hour=15, minute=35, second=0),
                      timezone=horo_timezone,
                      args=[bot])
    scheduler.start()
    scheduler_logger.info(f'Шедулер очистки дат запущен в {datetime.now()}')
