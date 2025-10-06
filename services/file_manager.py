import os
from typing import List

from utils.config import CLIENTS_DIR
from utils.logging_config import bot_logger


class DocumentManager:
    """
    Управляет папками с документами.
    Если начальный путь не указывается, то берется путь от текущего файла.
    """
    def __init__(self, start_path=None):
        self.start_path = start_path or os.path.dirname(os.path.abspath(__file__))

    def go_up_level_folder(self, levels=1):
        """
        Поднимаемся на уровни папок выше
        :param start_path: путь к текущему файлу
        :param levels: на сколько уровней подняться
        :return: абсолютный путь
        """
        path = os.path.abspath(self.start_path)
        for _ in range(levels):
            path = os.path.dirname(path)
        return path

    @staticmethod
    def go_to_folder(start_path, folder_name):
        """
        Переход к папке относительно start_path
        :param start_path: базовый путь
        :param folder_name: имя папки
        :return: абсолютный путь к папке
        """
        return os.path.join(os.path.abspath(start_path), folder_name)

    @staticmethod
    def show_all_folders(folder_path) -> List[str]:
        """
        Фильтрует папки, которые находятся в искомой папке и возвращает список.
        В список не попадают файлы, отличные от папок.
        :return: отфильтрованный список папок
        """
        try:
            return [item for item in os.listdir(folder_path)
                    if os.path.isdir(os.path.join(folder_path, item))]

        except PermissionError:
            bot_logger.exception(f"Нет доступа к папке: {folder_path}")
            return []

    def find_project_root(self, markers=['.git', 'requirements.txt']):
        """Находит корень проекта по маркерам"""
        current_path = os.path.abspath(self.start_path)  # получаем абсолютный путь к файлу

        while True:
            # Проверяем маркеры проекта
            for marker in markers:
                if os.path.exists(os.path.join(current_path, marker)):
                    return current_path

            # Поднимаемся на уровень выше
            parent_path = os.path.dirname(current_path)

            # Если достигли корневой директории
            if parent_path == current_path:
                break

            current_path = parent_path
        # Если маркеры не найдены, возвращаем стартовую директорию
        return os.path.dirname(os.path.abspath(self.start_path))


class FolderCleaner:
    """Класс отвечает за удаление ненужных папок"""
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.to_delete = []

    def is_folders_in_base_folder(self, folder_names: dict):
        """
        Сверяет, есть ли переданные подпапки в папке
        :param folder_names: словарь из папки и даты
        :return: список папок на удаление
        """
        for name, date in folder_names.items():
            if name in os.listdir(self.folder_path):
                self.to_delete.append(name)
                return self.folder_path

    @staticmethod
    def clean_folder(folder_path: str, folder_names: dict):
        """
        Удаление папок
        :param folder_path: путь к папке, где необходимо удалить ненужные папки
        :param folder_names: список наименований папок
        :return:
        """
        #  doc.show_all_folders(clients_dir)

        # folder_path = os.path.join(folder_path, folder_name)
        # print(folder_path)
        pass


doc = DocumentManager()
start_dir = doc.find_project_root()
clients_dir = doc.go_to_folder(start_dir, CLIENTS_DIR)
print(doc.show_all_folders(clients_dir))
