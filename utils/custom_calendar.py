import calendar
from datetime import date, timedelta
from utils.logging_config import bot_logger


month_names = {
                1: "январь", 2: "февраль", 3: "март",
                4: "апрель", 5: "май", 6: "июнь",
                7: "июль", 8: "август", 9: "сентябрь",
                10: "октябрь", 11: "ноябрь", 12: "декабрь"
            }


class MyCalendar:
    """
    Класс для работы с календарными данными.

    Хранит текущую дату и предоставляет методы для получения
    списка дней текущего, следующего и предыдущего месяцев.
    Также содержит метод для получения названия месяца на русском языке.
    """

    def __init__(self, day: date = date.today()):
        """
        Инициализация календаря.
        :param day: Дата, относительно которой будет строиться календарь.
                    По умолчанию используется текущая дата.
        """
        self.day = day
        self.month_list = []

    @classmethod
    def get_month_name(cls, day: date) -> str:
        """
        Возвращает название месяца на русском языке.
        :param day: Объект datetime.date.
        :return: Название месяца, например, "Январь".
        """
        return month_names.get(day.month, "")

    @classmethod
    def current_date_list(cls, day: date) -> list:
        """
        Формирует список дней для отображения в календаре.
        Включает дни предыдущего месяца и следующего месяца,
        чтобы календарь начинался с понедельника и заканчивался воскресеньем.
        """
        # Получаем первый и последний день месяца
        first_day = day.replace(day=1)
        last_day = day.replace(day=calendar.monthrange(day.year, day.month)[1])

        # Определяем день недели первого дня месяца (0-понедельник, 6-воскресенье)
        first_weekday = first_day.weekday()

        # Определяем день недели последнего дня месяца
        last_weekday = last_day.weekday()

        # Добавляем дни предыдущего месяца в начало
        calendar_days = []
        if first_weekday > 0:
            prev_month = first_day - timedelta(days=first_weekday)
            for i in range(first_weekday):
                calendar_days.append(prev_month + timedelta(days=i))

        # Добавляем дни текущего месяца
        current_month_days = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]
        calendar_days.extend(current_month_days)

        # Добавляем дни следующего месяца в конец
        days_to_add = 42 - len(calendar_days)  # Всего 42 дня в 6 неделях
        if days_to_add > 0:
            next_day = last_day + timedelta(days=1)
            for i in range(days_to_add):
                calendar_days.append(next_day + timedelta(days=i))

        return calendar_days

    @classmethod
    def next_month(cls, day: date) -> date:
        """
        Формирует список всех дней следующего месяца.
        Автоматически учитывает переход на новый год, если текущий месяц — декабрь.
        :param day: Объект datetime.date, по которому определяется следующий месяц.
        :return: Список объектов datetime.date для каждого дня следующего месяца.
        """
        if day.month == 12:
            next_month = date(day.year + 1, 1, 1)

        else:
            next_month = date(day.year, day.month + 1, 1)
        return next_month

    @classmethod
    def prev_month(cls, day: date) -> date:
        """
        Формирует список всех дней предыдущего месяца.
        Автоматически учитывает переход на предыдущий год, если текущий месяц — январь.
        :param day: Объект datetime.date, по которому определяется предыдущий месяц.
        :return: Список объектов datetime.date для каждого дня предыдущего месяца.
        """
        if day.month == 1:
            prev_month = date(day.year - 1, 12, 1)
        else:
            prev_month = date(day.year, day.month - 1, 1)
        return prev_month
