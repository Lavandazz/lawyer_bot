import os
import zipfile

from aiogram import Bot
from aiogram.fsm.context import FSMContext

from services.config import DOC_MAPPING, EXPECTED_DOCS
from utils.config import CLIENTS_DIR
from utils.logging_config import bot_logger


async def get_docs_from_state(state: FSMContext) -> dict:
    """
    Получает все документы из state data и возвращает словарь
    result: Словарь для наполнения. Как только документ загружен, он попадает в result.
    missing_docs: Список документов, которые осталось загрузить.
    """
    docs = await state.get_data()

    result = {}             # будет: {'contract': 'file123.jpg', 'comment': 'Срочно'}
    missing_docs = []       # будет: ['Скрин ЛК ВБ Джоб', 'Бейдж/пропуск'] - список отсутствующих документов

    for key, description in EXPECTED_DOCS.items():

        regular_value = docs.get(key)
        zip_value = docs.get(f"zip_{key}")  # получаем zip из data state

        # Документ считается загруженным если есть обычная версия ИЛИ ZIP версия
        value = regular_value or zip_value
        result[key] = value  # сохраняем в результат

        # Проверяем обязательные документы (кроме comment)
        if key != 'comment' and not value:  # если документ обязательный И отсутствует
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
    """
    Создание подпапки для документов в папке clients
    :param fio:
    :return folder_path
    """
    count = 1
    folder_path = os.path.join(CLIENTS_DIR, fio)  # clients\Иванов_и_и
    # Проверяем, существует ли папка с таким именем
    while os.path.exists(folder_path):
        string_path = folder_path.split("_")
        if string_path[-1].isdigit():
            name_folder, name_folder_count = string_path[:-1], int(string_path[-1]) + count
            name_folder = "_".join(name_folder)
            folder_path = f"{name_folder}_{name_folder_count}"
        else:
            # Если существует, добавляем суффикс с номером
            folder_path = f"{folder_path}_{count}"


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


async def save_zip_files(bot: Bot, folder_path: str, base_name: str, zip_doc_id: str) -> list:
    """
    Сохраняет и распаковывает ZIP архив
    Возвращает список путей к извлеченным файлам
    """
    try:
        # Сначала сохраняем ZIP файл временно
        temp_zip_path = await save_doc(bot, folder_path, "temp_archive", zip_doc_id)
        bot_logger.info(f"Сохранил zip: {temp_zip_path}")
        if not temp_zip_path:
            return []

        extracted_files = []

        # Распаковываем ZIP
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            bot_logger.info(f"Список файлов в zip {file_list}")

            for i, file_name in enumerate(file_list, 1):
                # Пропускаем папки
                if file_name.endswith('/'):
                    continue

                # Извлекаем расширение файла
                _, ext = os.path.splitext(file_name)
                new_filename = f"{base_name}_{i}{ext}"
                full_path = os.path.join(folder_path, new_filename)

                # Извлекаем файл
                with zip_ref.open(file_name) as source, open(full_path, 'wb') as target:
                    target.write(source.read())

                extracted_files.append(full_path)
                bot_logger.info(f"Извлечен файл {new_filename}")

        # Удаляем временный ZIP
        os.remove(temp_zip_path)
        return extracted_files

    except Exception as e:
        bot_logger.error(f"Ошибка при распаковке ZIP архива: {e}")
        return []


async def save_all_docs(bot: Bot, folder_path: str, docs: dict) -> dict:
    """
    Сохраняет все документы из словаря
    """
    file_paths = {}

    for state_key, file_name in DOC_MAPPING.items():
        print("state_key", state_key)
        # Получаем данные о документе
        doc_data = docs.get(state_key)  # убираем значение по умолчанию {}
        print("doc_data", doc_data)

        # Пропускаем если документ не передан
        if not doc_data:
            bot_logger.info(f"Документ {state_key} не передан, пропускаем")
            continue

        # Сохраняем ZIP архив
        if state_key.startswith("zip"):
            zip_paths = await save_zip_files(bot, folder_path, file_name, doc_data)
            print("zip_paths", zip_paths)
            file_paths[f"zip_{state_key}"] = zip_paths
            bot_logger.info(f"Сохранен ZIP архив {state_key}: {len(zip_paths)} файлов")

        else:
            file_path = await save_doc(bot, folder_path, file_name, doc_data)
            file_paths[state_key] = file_path

    return file_paths
