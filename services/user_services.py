from database.models_db import User
from utils.logging_config import db_logger


class UserServices:
    """
    Класс для управления данными пользователями
    """
    MODEL = None

    @classmethod
    async def get_users(cls, role):
        """Информация по пользователям, отфильтрованным по роли"""
        try:
            users = await User.filter(role=role).all()
            return users
        except Exception as e:
            db_logger.error(e)


