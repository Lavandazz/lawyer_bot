import logging
import os
from colorlog import ColoredFormatter


class BaseLogger:
    """ Базовый класс логгера """

    def __init__(self, name: str, log_file: str, logging_level=logging.INFO):
        self.name = name
        self.log_file = log_file
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging_level)  # настройка уровня логирования

        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """ Настройка обработчиков """
        # 1. Цветной вывод в консоль
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            '%(log_color)s%(levelname)-8s%(reset)s %(asctime)s [%(name)s] '
            '(%(filename)s).%(funcName)s(%(lineno)d) %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)

        # 2. Простой вывод в файл (без цветов)
        file_handler = logging.FileHandler(self.log_file, mode='a')
        file_formatter = logging.Formatter(
            '%(levelname)-8s %(asctime)s [%(name)s] '
            '(%(filename)s).%(funcName)s(%(lineno)d) %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # Добавляем обработчики
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.propagate = False  # чтобы aiogram не перекрывал логи, иначе видно только логи мидлваров

        # Логируем успешную настройку
        self.logger.info(f"Логирование для '{self.name}' настроено успешно.")

    def get_logger(self):
        """Возвращает настроенный логгер"""
        return self.logger


class BotLogger(BaseLogger):
    """Логгер для бота"""

    def __init__(self):
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(log_folder, "bot_logs.log")
        super().__init__(name="bot", log_file=log_file, logging_level=logging.DEBUG)


class HoroscopeLogger(BaseLogger):
    """ Логгер для гороскопа"""
    def __init__(self):
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(log_folder, "horo_logs.log")
        super().__init__(name="horoscope", log_file=log_file, logging_level=logging.DEBUG)


class HelpAiLogger(BaseLogger):
    """ Логгер для аи генератора"""
    def __init__(self):
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(log_folder, "phrase_logs.log")
        super().__init__(name="help_ai", log_file=log_file, logging_level=logging.DEBUG)


class DatabaseLogger(BaseLogger):
    """ Логгер для базы """
    def __init__(self):
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(log_folder, "db_logs.log")
        super().__init__(name="db", log_file=log_file)


class SchedulerLogger(BaseLogger):
    """ Логгер для шедулера """
    def __init__(self):
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(log_folder, "scheduler_logs.log")
        super().__init__(name="scheduler", log_file=log_file)


# Инициализация логгеров
bot_logger = BotLogger().get_logger()
horo_logger = HoroscopeLogger().get_logger()
db_logger = DatabaseLogger().get_logger()
scheduler_logger = SchedulerLogger().get_logger()
help_ai_logger = HelpAiLogger().get_logger()
