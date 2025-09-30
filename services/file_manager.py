from aiogram.fsm.context import FSMContext

from services.config import EXPECTED_DOCS
from services.file_detector import FileDetector
from utils.logging_config import bot_logger


class DocumentManager:
    """Управляет документами в состоянии FSM"""

    def __init__(self, state: FSMContext):
        self.state = state

    async def get_docs_from_state(self) -> dict:
        """
        Получает все документы из state data и возвращает словарь
        result: Словарь для наполнения. Как только документ загружен, он попадает в result.
        missing_docs: Список документов, которые осталось загрузить.
        """
        docs = await self.state.get_data()

        result = {}  # будет: {'contract': 'file123.jpg', 'comment': 'Срочно'}
        missing_docs = []  # будет: ['Скрин ЛК ВБ Джоб', 'Бейдж/пропуск'] - список отсутствующих документов

        for key, description in EXPECTED_DOCS.items():
            value = docs.get(key)  # получаем значение из state по ключу
            result[key] = value  # сохраняем в результат

            # Проверяем обязательные документы (кроме comment)
            if key != 'comment' and not value:  # если документ обязательный И отсутствует
                missing_docs.append(description)  # добавляем название документа в список отсутствующих

        # Устанавливаем комментарий по умолчанию
        if not result.get('comment'):
            result['comment'] = "pass"

        return {
            'docs': result,
            'missing': missing_docs,
            'is_complete': len(missing_docs) == 0
        }

    async def add_document_to_state(self, document: FileDetector, doc_key: str) -> None:
        """
        Добавление документа в state.data
        :param doc_key: название документа
        :return:
        """
        # Сохраняем словарь с информацией о файле
        # file_info = {
        #     'file_id': document.file_id,
        #     'is_zip': document.is_zip()
        # }
        # await self.state.update_data({file_name: file_info})

        if document.is_zip():
            key = f"zip_{doc_key}"
        else:
            key = doc_key

        await self.state.update_data({key: document.file_id})

        bot_logger.info(f"Документ {doc_key} добавлен: {document.file_id}")
        bot_logger.info(f"Документ {document} добавлен в state data: {document.file_id}")

    async def is_uploaded(self, doc_key: str) -> bool:
        """Проверяет, загружен ли документ"""
        data = await self.state.get_data()
        return bool(data.get(doc_key) or data.get(f"zip_{doc_key}"))

    async def add_comment_to_state(self, comment: str) -> None:
        """Добавляет комментарий в state"""
        await self.state.update_data({'comment': comment})
        bot_logger.info(f"Комментарий добавлен в state: {comment}")
