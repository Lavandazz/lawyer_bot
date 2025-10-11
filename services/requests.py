from dateutil.relativedelta import *
import datetime

from database.config import RequestStatus
from database.models_db import SalaryRequest
from utils.logging_config import bot_logger, db_logger


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
        try:
            requests = await SalaryRequest.filter(status=status).all()
            return requests
        except Exception as e:
            db_logger.error(f"Ошибка получения заявки: {e}")

    @classmethod
    async def get_user_requests_by_id(cls, user_id: int = None, telegram_id: int = None):
        """
        Все заявки отфильтрованные по пользователю
        :param user_id: id пользователя
        :return: requests
        """
        try:
            if user_id:
                requests = await SalaryRequest.filter(user_id=user_id).all()
                return requests
            else:
                requests = await SalaryRequest.filter(
                    user__telegram_id=telegram_id  # Двойное подчеркивание для связи
                ).prefetch_related('user').all()
                return requests
        except Exception as e:
            db_logger.error(f"Ошибка получения заявки: {e}")

    @classmethod
    async def get_user_request(cls, request_id):
        """
        Фильтрация заявки по id
        :param request_id: id заявки
        :return:
        """
        try:
            request = await SalaryRequest.filter(id=request_id).prefetch_related('user').first()
            return request
        except Exception as e:
            db_logger.error(f"Ошибка получения заявки: {e}")

    @classmethod
    async def requests_by_status(cls, status: RequestStatus) -> dict[str, datetime.date]:
        """
        Фильтрация заявки по статусу
        :param status: статус заявки RequestStatus.PENDING/APPROVED/REJECTED
        :return:
        """
        try:
            requests = await SalaryRequest.filter(status=status).all()
            rejected_list = {request.user_folder: request.date_to_delete for request in requests}
            return rejected_list
        except Exception as e:
            db_logger.error(f"Ошибка фильтрации заявок: {e}")

    @classmethod
    async def requests_by_date_to_delete(cls, date_to_del) -> list[str] | str:
        """
         Фильтрация заявок для дальнейшего удаления. Фильтруем заявки по статусу отказа и дате от текущего число
         :param target_date: дата, по месяцу которой фильтруем
         :return: список название папок
         """
        try:
            date_to_del += relativedelta(months=+1)

            requests = await SalaryRequest.filter(
                status=RequestStatus.REJECTED,
                deleted=False,
                date_to_delete__gt=date_to_del).all()

            rejected_list = [request.user_folder for request in requests]
            return rejected_list

        except Exception as e:
            db_logger.error(f"Ошибка фильтрации заявок: {e}")
            return f'ошибка {e}'

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
            db_logger.info(f"Статус заявки {request_id} изменен: {status}")

            return True, user.telegram_id

        except Exception as e:
            db_logger.exception(f"Не получилось изменить статус заявки {request_id}: {e}")
            return False

    @staticmethod
    async def mark_to_delete(folder_name: str):
        """
        Пометить папку на удаление
        :return:
        """
        try:
            await SalaryRequest.filter(user_folder=folder_name).update(deleted=True)
            db_logger.info(f"Изменил поле deleted для папки {folder_name}")
        except Exception as e:
            db_logger.error(f"не получилось пометить на удаление папку {folder_name}: {e}")


class RequestService(BaseRequestService):
    MODEL = SalaryRequest
