from tortoise import fields
from tortoise.models import Model

from database.config import RequestStatus


class User(Model):
    """
    Модель для сохранения пользователей.
    Поля: никнейм, имя, фамилия, id, роль, дата регистрации, последняя активность с ботом, статус(active\block)
    """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, null=True)
    patronymic = fields.CharField(max_length=100, null=True)
    first_name = fields.CharField(max_length=100, null=True)
    second_name = fields.CharField(max_length=100, null=True)
    phone = fields.BigIntField(unique=True)
    telegram_id = fields.BigIntField(unique=True)
    role = fields.CharField(max_length=20, default='user')
    registration_date = fields.DatetimeField(auto_now_add=True)
    last_activity = fields.DatetimeField(null=True)
    status = fields.CharField(max_length=20, default='active')

    class Meta:
        table = 'users'


class AdminPost(Model):
    """
    Модель бд для отображения постов админа
    """
    id = fields.IntField(pk=True)
    # models берется из config
    user_id: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User',
                                                                      related_name='posts',
                                                                      source_field="user_id")
    photo_file_id = fields.CharField(max_length=255, null=True)
    text = fields.TextField()
    date = fields.DatetimeField(auto_now_add=True)
    status = fields.IntField(default=0)

    class Meta:
        table = 'admin_posts'


class SalaryRequest(Model):
    """
    Модель для загрузки данных по вопросам отпускных.
    contract - трудовой договор.
    account_screenshot - скрин из лк приложения ВБ Джоб.
    a_pass - бейдж, пропуск.
    ndfl_reference - 2 НДФЛ.
    extract - выписка из индивидуального лицевого счета.
    employment_record - трудовая книжка.
    comment - комментарий, возможно оставить пустым.
    approved - статус, принят ли в работу.
    user_folder - название папки.
    created_at - дата создания запроса.
    status - обозначает статус заявки.
    date_to_delete - дата для удаления шедулером. (+30 дней с момента отклонения)
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        'models.User',
        related_name='salary_requests')
    contract = fields.CharField(max_length=255, null=True)
    account_screenshot = fields.CharField(max_length=255, null=True)
    a_pass = fields.CharField(max_length=255, null=True)
    ndfl_reference = fields.CharField(max_length=255, null=True)
    extract = fields.CharField(max_length=255, null=True)
    employment_record = fields.CharField(max_length=255, null=True)
    comment = fields.TextField(null=True)
    approved = fields.BooleanField(default=False)
    user_folder = fields.CharField(max_length=300, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    reject_comment = fields.CharField(max_length=255, null=True)
    status = fields.IntField(
        default=RequestStatus.PENDING.value,
        choices=[
            (RequestStatus.PENDING.value, "На рассмотрении"),
            (RequestStatus.APPROVED.value, "Одобрено"),
            (RequestStatus.REJECTED.value, "Отклонено")
        ])
    date_to_delete = fields.DateField(null=True)
    passport = fields.BooleanField(default=False)

    class Meta:
        table = 'salary_requests'


class Statistic(Model):
    """
    Класс хранит статистику по новым пользователям, а так же по количеству использований бота.
    """
    id = fields.IntField(pk=True)
    day = fields.DateField(unique=True)
    new_user = fields.IntField(default=0)
    event = fields.IntField(default=0)

    class Meta:
        table = 'statistics'


