from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Настройка пути к .env
ENV_MODE = "local"  # Менять на "production" для основного .env
env_file = ".env.local" if ENV_MODE == "local" else ".env"
env_path = PROJECT_ROOT / env_file

# Загрузка переменных окружения
load_dotenv(dotenv_path=env_path)
