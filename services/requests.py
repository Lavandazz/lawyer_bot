from datetime import datetime

from database.config import RequestStatus
from database.models_db import SalaryRequest
from utils.logging_config import bot_logger


class BaseRequestService:
    """
    Класс для получаения данных из бд по заявкам
    """
    MODEL = None

    @classmethod
    async def get_requests(cls, status):
        """
        Все заявки отфильтрованные по статусу
        :param status: передаем статус RequestStatus.PENDING/APPROVED/REJECTED
        :return: requests
        """
        requests = await SalaryRequest.filter(status=status).all()
        return requests

    @classmethod
    async def get_user_requests_by_id(cls, user_id: int = None, telegram_id: int = None):
        """
        Все заявки отфильтрованные по пользователю
        :param user_id: id пользователя
        :return: requests
        """
        if user_id:
            requests = await SalaryRequest.filter(user_id=user_id).all()
            return requests
        else:
            requests = await SalaryRequest.filter(
                user__telegram_id=telegram_id  # Двойное подчеркивание для связи
            ).prefetch_related('user').all()
            return requests

    @classmethod
    async def get_user_request(cls, request_id):
        """
        Фильтрация заявки по id
        :param request_id: id заявки
        :return:
        """
        request = await SalaryRequest.filter(id=request_id).prefetch_related('user').first()
        return request

    @classmethod
    async def requests_by_status(cls, status: RequestStatus) -> dict[str, datetime.date]:
        """
        Фильтрация заявки по статусу
        :param status: статус заявки RequestStatus.PENDING/APPROVED/REJECTED
        :return:
        """
        requests = await SalaryRequest.filter(status=status).all()
        rejected_list = {request.user_folder: request.date_to_delete for request in requests}
        return rejected_list

    @classmethod
    async def change_status_request(cls, request_id: int, status: int, comment: str = None) -> tuple | bool:
        """
        Изменение статуса заявки в бд
        :param request_id: int
        :return: bool
        """
        try:
            request = await cls.get_user_request(request_id=request_id)
            user = request.user

            if status == RequestStatus.REJECTED:
                request.reject_comment = comment
                request.status = RequestStatus.REJECTED

            elif status == RequestStatus.APPROVED:
                request.status = RequestStatus.APPROVED
            else:
                pass

            await request.save()
            bot_logger.info(f"Статус заявки {request_id} изменен: {status}")

            return True, user.telegram_id

        except Exception as e:
            bot_logger.exception(f"Не получилось изменить статус заявки {request_id}: {e}")
            return False


class RequestService(BaseRequestService):
    MODEL = SalaryRequest


