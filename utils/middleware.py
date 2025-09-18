from aiogram.types import TelegramObject
from redis.asyncio import Redis
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any
from datetime import date, datetime

from tortoise.exceptions import DoesNotExist

from database.models_db import User, Statistic
from utils.logging_config import bot_logger


class RoleMiddleware(BaseMiddleware):
    """
    Middleware для обработки каждого события от пользователя.

    Функция выполняет:
    1. Определение пользователя по telegram_id.
    2. Если пользователь найден в базе — обновление времени его последней активности.
    3. Если пользователь не найден — создание нового пользователя с ролью "user".
    4. Запись в словарь data:
       - "role": роль пользователя.
       - "new_user": True, если пользователь зарегистрирован в этот момент, иначе False.

    После обработки передает управление следующему хендлеру в цепочке.
    """
    async def __call__(self, handler, event, data):
        try:
            user_id = event.from_user.id  # 7599073638
            user = await User.get_or_none(telegram_id=user_id)
            # bot_logger.debug(f'Пользователь взаимодействует с ботом {user_id}')

            if user:
                # Если есть в базе — обновляем активность
                user.last_activity = datetime.now()
                await user.save()
                data["role"] = user.role
                data["new_user"] = False
            else:

                bot_logger.debug(f"Новый пользователь {user_id}")
                data["new_user"] = True
                data["role"] = "user"

        except Exception as e:
            bot_logger.exception(e)

        return await handler(event, data)


class StatisticMiddleware(BaseMiddleware):
    """
    Этот мидлвар записывает статистику посещений бота.
    Работа происходит через Redis базу. Создается пара Ключ - телеграм айди юзера: Значение - дата.
    Если пользователь уже заходил в бота в текущий день, то апдейт уже не учитывается.
    В бд постгрес сохраняется общее количество апдейтов за день.
    А так же, если был новый пользователь, то он тоже сохраняется в бд.
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def __call__(self,
                       handler: Callable,
                       event: TelegramObject,
                       data: Dict[str, Any]):

        user_id = event.from_user.id
        user = await User.get_or_none(telegram_id=user_id)
        event_date = date.today()

        redis_key = f'user{user_id}:visit'
        # bot_logger.debug(f'redis_key : {redis_key}')

        try:

            # Создание в бд строки с датой
            stat, create_state = await Statistic.get_or_create(day=event_date)
            # bot_logger.debug(f'stat создался при апдейте: {stat}{create_state}.\n'
            #                  f'redis_key : {redis_key} = {await self.redis.get(redis_key)}\n'
            #                  f'{await self.redis.exists(redis_key)}')
            # Если юзера нет в бд, то добавляется +1 new_user
            if not user:
                stat.new_user += 1
                # bot_logger.debug(f"stat.new_user увеличен до {stat.new_user}")

            # Проверяем, есть ли в базе ключ redis_key, то есть заходил ли пользователь
            if not await self.redis.exists(redis_key):
                # Устанавливаем ключ с TTL до конца суток (24 часа)
                await self.redis.set(redis_key, "1", ex=60 * 60 * 24)
                # Сохраняем в бд
                stat.event += 1
                # bot_logger.debug(f"stat.event увеличен до {stat.event}")

            try:
                await stat.save()
                # bot_logger.debug(f"статистика сохранена event = {stat.event}, new_user = {stat.new_user}")
            except Exception as e:
                bot_logger.error(f"[Ошибка сохранения в БД]: {e}")
            #
            # keys = await self.redis.keys("user*")
            # print(len(keys))
            # for key in keys:
            #     value = await self.redis.get(key)
            #     print(f"Все юзеры {key}: {value}")

        except Exception as e:
            bot_logger.error(f"[StatisticMiddleware] Ошибка статистики: {e}")

        # Передаём управление дальше в функции
        return await handler(event, data)
