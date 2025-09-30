import zipfile
import os
from utils.logging_config import bot_logger


class ArchiveProcessor:
    """Обрабатывает ZIP архивы"""

    def __init__(self):
        # Словарь для подсчета файлов каждого типа
        self.file_counters = {}

    def _get_file_extension(self, filename):
        """Просто возвращает расширение файла"""
        return os.path.splitext(filename)[1].lower()

    def _get_next_number(self, extension):
        """Возвращает следующий номер для этого расширения"""
        if extension not in self.file_counters:
            self.file_counters[extension] = 0
        self.file_counters[extension] += 1
        return self.file_counters[extension]

    def process_archive(self, archive_path, extract_to_folder):
        """
        Распаковывает архив и нумерует файлы по их расширениям
        """
        extracted_files = []

        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                for file_info in zip_file.filelist:
                    # Пропускаем папки
                    if file_info.is_dir():
                        continue

                    # Получаем расширение файла
                    extension = self._get_file_extension(file_info.filename)
                    if not extension:  # если нет расширения
                        extension = '.file'

                    # Получаем номер для этого расширения
                    file_number = self._get_next_number(extension)

                    # Создаем простое имя: тип_номер.расширение
                    file_type = extension[1:] if extension.startswith('.') else extension
                    new_filename = f"{file_type}_{file_number}{extension}"
                    new_file_path = os.path.join(extract_to_folder, new_filename)

                    # Извлекаем файл
                    with zip_file.open(file_info.filename) as source_file:
                        with open(new_file_path, 'wb') as target_file:
                            target_file.write(source_file.read())

                    extracted_files.append(new_file_path)
                    bot_logger.info(f"Извлечен: {file_info.filename} -> {new_filename}")

            bot_logger.info(f"Архив распакован: {len(extracted_files)} файлов")
            return extracted_files

        except Exception as e:
            bot_logger.error(f"Ошибка распаковки архива {archive_path}: {e}")
            return []