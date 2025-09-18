from datetime import date
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.custom_calendar import MyCalendar


async def calendar_kb(calendar_day: date) -> InlineKeyboardMarkup:
    """
    Создаёт inline-клавиатуру календаря.

    :param calendar_day: Дата, для которой отображается календарь
    :return: Объект InlineKeyboardMarkup с разметкой календаря
    """
    calendar_obj = MyCalendar(calendar_day)
    days = MyCalendar.current_date_list(calendar_day)
    month_name = MyCalendar.get_month_name(calendar_day)

    # Билдер для дней
    days_builder = InlineKeyboardBuilder()

    # Добавляем заголовки дней недели
    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for day_name in week_days:
        days_builder.button(text=day_name, callback_data="ignore")

    # Добавляем кнопки с днями
    for d in days:
        if d.month == calendar_day.month:
            # Дни текущего месяца
            days_builder.button(
                text=d.strftime('%d'),
                callback_data=f"day_{d.strftime('%d.%m.%Y')}"
            )
        else:
            # Дни других месяцев (бледные)
            days_builder.button(
                text=f"·{d.strftime('%d')}·",
                callback_data=f"day_{d.strftime('%d.%m.%Y')}"
            )

    # Разбиваем на ряды: 7 дней в неделе
    days_builder.adjust(7, *[7] * 6)  # 1 ряд заголовков + 6 рядов дней

    # Финальный билдер
    kb = InlineKeyboardBuilder()

    # Шапка с навигацией
    kb.row(
        InlineKeyboardButton(text='⬅️', callback_data='prev_month'),
        InlineKeyboardButton(text=month_name, callback_data='current_month'),
        InlineKeyboardButton(text='➡️', callback_data='next_month'),
    )

    # Прикрепляем дни
    kb.attach(days_builder)

    # Кнопка выхода
    kb.row(InlineKeyboardButton(text='❌ Выход', callback_data='back'))

    return kb.as_markup()