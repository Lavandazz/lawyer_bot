from datetime import datetime

from services.file_manager import DocumentManager
from services.requests import RequestService
from utils.config import CLIENTS_DIR

doc = DocumentManager()


async def filter_name_folders() -> list[str]:
    """
    Получение списка путей папок для очистки.

    :return: Список из путей к папкам, которые необходимо удалить.
    """
    now = datetime.now()
    # получаем список из бд
    reqs = await RequestService.requests_by_date_to_delete(now)
    # получаем пути к папке clients
    start_dir = doc.find_project_root()
    clients_dir = doc.go_to_folder(start_dir, CLIENTS_DIR)
    folders = set(doc.show_all_folders(clients_dir))
    # проверяем есть ли названия папок из бд в папке clients
    folders_to_del = [folder for folder in reqs if folder in folders]
    result_folders = [doc.go_to_folder(clients_dir, folder) for folder in folders_to_del]

    return result_folders





