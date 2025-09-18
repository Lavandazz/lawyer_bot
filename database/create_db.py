from tortoise import Tortoise
from .tortoise_config import TORTOISE_ORM
from dotenv import load_dotenv

load_dotenv()


async def init_db():
    await Tortoise.init(
        config=TORTOISE_ORM,  # передаем конфиг
        modules={
            'users': ['users.models_db'],
            'salary_requests': ['salary_requests.models_db'],
            'admin_posts': ['admin_posts.models_db'],
            'statistics': ['statistics.models_db'],
        }
    )
    await Tortoise.generate_schemas()  # создание таблиц, если их нет


async def close_db():
    await Tortoise.close_connections()
