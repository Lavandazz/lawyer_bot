from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    """ Главное меню"""
    main_menu = State()
    admin_menu = State()


class UserState(StatesGroup):
    register = State()
    phone = State()
    all_requests = State()
    request = State()


class AnswerState(StatesGroup):
    all_questions = State()
    docs_questions = State()
    doc_answer = State()
    answer = State()


class CreateRequest(StatesGroup):
    wait_contract = State()
    wait_acc_screenshot = State()
    wait_personal_pass = State()
    wait_ndfl = State()
    wait_extract = State()
    wait_record_book = State()
    wait_comment = State()
    save = State()


class AdminMenuState(StatesGroup):
    """ Меню админа """
    requests_menu = State()
    request = State()
    statistic_menu = State()  # меню статистики
    statistic = State()


class StatsState(StatesGroup):
    """Статистика"""
    waiting_date = State()
    waiting_first_date = State()
    waiting_second_date = State()
    answer = State()


class ApproveState(StatesGroup):
    reject_comment = State()


# class BaristaState(StatesGroup):
#     """ Меню бариста """
#     menu = State()
#     games_menu = State()
#     posts_menu = State()
#     review_menu = State()
#     approve_menu = State()
#     posts = State()  # отображение всех постов
#     post = State()  # отображение поста
#
#
# class BaristaRegistrationState(StatesGroup):
#     """Регистрация бариста"""
#     registration_name = State()
#     save_name = State()
#     delete_name = State()


# class AdminRegistrationState(StatesGroup):
#     """Регистрация бариста"""
#     waiting_choice = State()
#     search_name = State()
#     save_name = State()
#     delete_name = State()
#
#
# class PostState(StatesGroup):
#     """ Действия, связанные с регистрацией поста """
#     add_post = State()  # добавление поста
#     register_text = State()  # добавление текста
#     generated_text = State()  # генерация текста AI
#     editing_text = State()  # изменение текста поста
#     save_post = State()  # сохранение поста

#
# class RequestStates(StatesGroup):
#     """ Добавление отзыва клиентом """
#     waiting_for_photo = State()
#     waiting_for_text = State()
