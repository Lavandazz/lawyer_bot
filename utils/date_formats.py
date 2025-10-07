from datetime import date


def from_str_to_date_day(date_string: str) -> date:
    """Преобразование строки даты в формат date для дальнейшего использования в бд"""
    if date_string != "back":
        list_date = date_string.split('_')[1].split('.')
        call_date = list(map(int, list_date))
        return date(year=call_date[2], month=call_date[1], day=call_date[0])


def date_game_saver(day: date) -> bool:
    """Проверка даты игры. Если дата больше текущей, то возвращается True."""
    if day > date.today():
        return True
    else:
        return False
