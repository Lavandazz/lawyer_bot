from aiogram.types import Message

DICT_TYPE = {
    "zip": "zip",
    "pdf": "pdf",
    "png": "image",
    "jpg": "image",
    "jpeg": "image"
}


class FileDetector:
    """
    Класс определяет тип получаемого документа/фото.
    """

    def __init__(self, message: Message):
        # принимаем файл (документ, фото, zip)
        self.message = message
        self._file_type = None
        self._file_id = None

        # вызываем метод для инициации
        self._get_file()

    def _get_file(self):
        """
        Определение типа файла
        """
        if self.message.document:
            self._file_id = self.message.document.file_id
            self._file_type = DICT_TYPE.get(self.message.document.file_name.split(".")[1])

        elif self.message.photo:
            self._file_id = self.message.photo[-1].file_id
            self._file_type = "image"

    @property
    def file_type(self):
        return self._file_type

    @property
    def file_id(self):
        return self._file_id

    # Метод для проверки, является ли сообщение файлом
    def is_file(self):
        return bool(self.message.document or self.message.photo)

    def is_zip(self):
        """Проверяем, это ZIP архив или нет"""
        return self.file_type == "zip"


