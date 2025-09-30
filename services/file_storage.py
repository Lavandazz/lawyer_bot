import os

from aiogram import Bot

from services.config import DOC_MAPPING
from utils.config import CLIENTS_DIR
from utils.logging_config import bot_logger


class FileStorage:
    """
    Класс для сохранения файлов на диск
    """
    def __init__(self, base_path: str = CLIENTS_DIR):
        self.base_path = base_path

    @staticmethod
    def create_folder(fio: str) -> str:
        """
        Создание подпапки для документов в папке clients
        :param fio:
        :return folder_path путь к созданной папке
        """
        count = 1
        folder_path = os.path.join(CLIENTS_DIR, fio)
        # Проверяем, существует ли папка с таким именем
        while os.path.exists(folder_path):
            # Если существует, добавляем суффикс с номером
            folder_path = f"{folder_path}_{count}"
            count += 1

        # Создаем папку
        os.makedirs(folder_path, exist_ok=True)
        bot_logger.info(f"Создана папка {folder_path}")
        return folder_path

    @staticmethod
    async def save_document(bot: Bot, folder_path: str, name: str, doc_id: str) -> str | None:
        """
        Сохранение файла из Telegram на диск
        :param bot: экземпляр бота
        :param folder_path: путь к папке для сохранения
        :param name: Название файла
        :param doc_id: file_id телеграмм
        :return: путь к сохраненному файлу
        """
        try:
            # Получаем информацию о файле
            file_info = await bot.get_file(doc_id)
            file_path = file_info.file_path

            # Скачиваем файл
            downloaded_file = await bot.download_file(file_path)

            # Формируем имя файла
            file_extension = os.path.splitext(file_path)[1] or '.dat'
            filename = f"{name}{file_extension}"
            full_path = os.path.join(folder_path, filename)

            # Сохраняем файл
            with open(full_path, 'wb') as new_file:
                # Если это bytes - пишем как есть, если файловый объект - читаем
                if isinstance(downloaded_file, bytes):
                    new_file.write(downloaded_file)
                else:
                    # Для файловых объектов читаем содержимое
                    content = downloaded_file.read()
                    new_file.write(content)

            bot_logger.info(f"Файл {filename} сохранен в {folder_path}")
            return full_path

        except Exception as e:
            bot_logger.error(f"Ошибка при сохранении файла {name}: {e}")
            return None

    async def save_all_docs(self, bot: Bot, folder_path: str, docs: dict) -> dict:
        """
        Сохраняет все документы из словаря
        """
        file_paths = {}

        for state_key, file_name in DOC_MAPPING.items():
            doc_id = docs.get(state_key)
            if doc_id:
                file_path = await self.save_document(bot, folder_path, file_name, doc_id)
                file_paths[state_key] = file_path

        return file_paths
