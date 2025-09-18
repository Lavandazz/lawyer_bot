import os
from utils.settings_env import env_file


# настройка подключения к бд через TORTOISE
DATABASE_URL = (
    f"postgres://{os.getenv('DATABASE_USER')}:"
    f"{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{int(os.getenv('DATABASE_PORT'))}/"
    f"{os.getenv('DATABASE_NAME')}"
)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["database.models_db", "aerich.models"],  # aerich.models миграции
            "default_connection": "default",
        },
    },
}
