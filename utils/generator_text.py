import random

coffee_greetings = {
    "morning": [
        "☀️ Доброе утро!"
    ],
    "day": [
        "🌞 Добрый день!"
    ],
    "evening": [
        "🌙 Добрый вечер!"
    ]
}


def generate_day_or_night(now_time: int):
    if 5 < now_time < 13:
        return random.choice(coffee_greetings["morning"])
    elif 12 < now_time < 19:
        return random.choice(coffee_greetings["day"])
    else:
        return random.choice(coffee_greetings["evening"])