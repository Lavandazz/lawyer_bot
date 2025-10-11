import os
import shutil

from services.cleaner import filter_name_folders
from services.requests import RequestService
from utils.config import admin_id, bot, SUPERADMIN

from aiogram import Bot
from aiogram.types import CallbackQuery
from pytz import timezone
from datetime import datetime, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.logging_config import scheduler_logger, cleaner_logger


def get_first_day_next_month() -> date:
    """
    Вычисление первого дня следующего месяца для очистки базы
    :return: next_month - первый день следующего месяца
    """
    today = datetime.now().date()
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    return next_month
    # return datetime(2025, 6, 3).date()


async def delete_folders():
    """
    Получение данных для удаления.
    """
    folders_to_delete = await filter_name_folders()
    scheduler_logger.info(f"Получил папки для удаления {folders_to_delete}")
    try:
        if folders_to_delete:
            for folder in folders_to_delete:
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                    folder_name = os.path.basename(folder)
                    await RequestService.mark_to_delete(folder_name)
                    cleaner_logger.info(f'Удаление папки {folder_name}')

    except Exception as e:
        await bot.send_message(chat_id=SUPERADMIN, text=f'Очистка папок клиентов не проведена : {e}')
        scheduler_logger.warning(f'Ошибка при очистке дат гороскопа {datetime.now()}, {e}')


async def scheduler_clean_folders():
    """
    Шедулер для очистки удаления ненужны папок.
    Шедулер запускается на основании вычисленной даты next_month
    и запускается автоматически в первый день месяца в 15 часов 35 минут.

    """
    next_month = get_first_day_next_month()
    t_timezone = timezone('Europe/Moscow')
    scheduler = AsyncIOScheduler()

    scheduler.add_job(delete_folders, "date",
                      run_date=datetime(year=next_month.year, month=next_month.month, day=1, hour=15, minute=35, second=0),
                      timezone=t_timezone
                      )
    scheduler.start()
    scheduler_logger.info(f'Шедулер очистки папок запущен в {datetime.now()}')
