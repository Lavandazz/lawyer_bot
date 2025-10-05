from enum import Enum


class RequestStatus(int, Enum):
    PENDING = 0    # на рассмотрении
    APPROVED = 1   # одобрено
    REJECTED = 2   # отклонено