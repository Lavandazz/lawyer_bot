import os

from aiogram import Bot
from aiogram.fsm.context import FSMContext

from utils.config import CLIENTS_DIR
from utils.logging_config import bot_logger


async def get_docs_from_state(state: FSMContext) -> dict:
    """
    Получает все документы из state data и возвращает словарь
    """
    docs = await state.get_data()

    # Словарь с ожидаемыми документами
    expected_docs = {
        'contract': 'Договор',
        'acc_screenshot': 'Скриншот счета',
        'personal_pass': 'Паспорт',
        'extract': 'Выписка',
        'ndfl': 'Справка 2-НДФЛ',
        'record_book': 'Трудовая книжка',
        'comment': 'Комментарий',
    }

    result = {}
    missing_docs = []

    for key, description in expected_docs.items():
        value = docs.get(key)
        result[key] = value

        # Проверяем обязательные документы (кроме comment)
        if key != 'comment' and not value:
            missing_docs.append(description)

    # Устанавливаем комментарий по умолчанию
    if not result.get('comment'):
        result['comment'] = "pass"

    return {
        'docs': result,
        'missing': missing_docs,
        'is_complete': len(missing_docs) == 0
    }


def create_folder(fio: str) -> str:
    """Создание подпапки для документов в папке clients"""
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


async def save_doc(bot: Bot, folder_path: str, name: str, doc_id: str) -> str | None:
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


async def save_all_docs(bot: Bot, folder_path: str, docs: dict) -> dict:
    """
    Сохраняет все документы из словаря
    """
    file_paths = {}
    doc_mapping = {
        'contract': 'contract',
        'acc_screenshot': 'screenshot',
        'personal_pass': 'personal_pass',
        'extract': 'extract',
        'ndfl': 'ndfl',
        'record': 'record'
    }

    for state_key, file_name in doc_mapping.items():
        doc_id = docs.get(state_key)
        if doc_id:
            file_path = await save_doc(bot, folder_path, file_name, doc_id)
            file_paths[state_key] = file_path

    return file_paths
