from aiogram import Dispatcher, F
from aiogram.filters import Command, StateFilter

from handlers.admin.get_statistic_handlers import get_statistic, get_period_statistic, day_statistic, \
    first_day_statistic, second_day_statistic, prev_month, next_month
from handlers.admin.users_requests import show_requests, show_user_request
from handlers.back.back_handler import back, clear_message
from handlers.user.create_request.acc_screenshot import creating_request_acc_screenshot_save, \
    creating_request_acc_screenshot
from handlers.user.create_request.comment import creating_request_comment, creating_request_comment_save
from handlers.user.create_request.contract import creating_contract, creating_contract_save
from handlers.user.create_request.extract import creating_request_extract_save, creating_request_extract
from handlers.user.create_request.ndfl import creating_request_ndfl, creating_request_ndfl_save
from handlers.user.create_request.personal_pass import creating_request_pass_save, creating_request_pass
from handlers.user.create_request.record import creating_request_record_book_save, creating_request_record_book
from handlers.user.create_request.surname import creating_request_surname, creating_request_surname_save

from handlers.user.help_handlers import get_help, hide_faq_handler, get_help_docs, get_help_how_upload, answer
from handlers.user.registeration import process_contact, approve_phone, start_registration_user_name
from handlers.user.start_handlers import get_start, on_start
from handlers.admin.admin_handlers import admin_menu

from handlers.cancel_state_handler import cancel_handler
from handlers.user.user_lk_requests import user_lk, show_my_request
from handlers.user.user_request_handlers import creating_request, creating_request_save

from states.menu_states import StatsState, CreateRequest, UserState
from utils.middleware import RoleMiddleware, StatisticMiddleware

from utils.config import redis_client


def setup_dispatcher(dp: Dispatcher):
    """ Регистрация роутеров бота """
    dp.startup.register(on_start)
    # мидлвары
    dp.message.middleware(StatisticMiddleware(redis_client))
    dp.callback_query.middleware(StatisticMiddleware(redis_client))
    dp.message.middleware(RoleMiddleware())
    dp.callback_query.middleware(RoleMiddleware())

    # команды
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(cancel_handler, Command(commands='cancel'))
    dp.message.register(get_help, Command(commands='help'))

    # регистрация фио и телефона
    dp.message.register(start_registration_user_name, StateFilter(UserState.register))
    dp.message.register(process_contact, F.contact)
    dp.callback_query.register(approve_phone, F.data.startswith("approve_"))

    # help
    dp.callback_query.register(get_help_docs, F.data == "what_upload")
    dp.callback_query.register(get_help_how_upload, F.data.startswith("how_"))
    dp.callback_query.register(answer, F.data.startswith("get_"))

    # оформление запроса пользователя
    dp.callback_query.register(creating_request, F.data == "start_request")

    dp.callback_query.register(creating_contract, F.data == "contract")
    dp.message.register(creating_contract_save, F.document | F.photo,  StateFilter(CreateRequest.wait_contract))

    dp.callback_query.register(creating_request_acc_screenshot, F.data == "acc_screenshot")
    dp.message.register(creating_request_acc_screenshot_save, F.photo, StateFilter(CreateRequest.wait_acc_screenshot))

    dp.callback_query.register(creating_request_pass, F.data == "personal_pass")
    dp.message.register(creating_request_pass_save, F.photo, StateFilter(CreateRequest.wait_pass))

    dp.callback_query.register(creating_request_ndfl, F.data == "ndfl")
    dp.message.register(creating_request_ndfl_save, F.document | F.photo, StateFilter(CreateRequest.wait_ndfl))

    dp.callback_query.register(creating_request_extract, F.data == "extract")
    dp.message.register(creating_request_extract_save, F.document | F.photo, StateFilter(CreateRequest.wait_extract))

    dp.callback_query.register(creating_request_record_book, F.data == "record_book")
    dp.message.register(creating_request_record_book_save, F.document | F.photo, StateFilter(CreateRequest.wait_record_book))

    dp.callback_query.register(creating_request_comment, F.data == "comment")
    dp.message.register(creating_request_comment_save, F.text, StateFilter(CreateRequest.wait_comment))

    dp.callback_query.register(creating_request_save, F.data == "send")

    dp.callback_query.register(clear_message, F.data.startswith('clear_'))

    dp.callback_query.register(user_lk, F.data == "my_requests")
    dp.callback_query.register(show_my_request, F.data.startswith("user_request_"))
    # панель администратора
    dp.callback_query.register(admin_menu, F.data == "admin_panel")
    dp.callback_query.register(show_requests, F.data == "requests")
    dp.callback_query.register(show_user_request, F.data.startswith("admin_request_"))
    dp.callback_query.register(get_statistic, F.data == 'statistic')

    # # календарь
    dp.callback_query.register(get_period_statistic, F.data.startswith('stat_'))
    dp.callback_query.register(prev_month, F.data == "prev_month")
    dp.callback_query.register(next_month, F.data == "next_month")
    dp.callback_query.register(day_statistic, StateFilter(StatsState.waiting_date))
    dp.callback_query.register(first_day_statistic, StateFilter(StatsState.waiting_first_date))
    dp.callback_query.register(second_day_statistic, StateFilter(StatsState.waiting_second_date))
    #
    # dp.callback_query.register(clear_message,  F.data.startswith('clear_'))
    #
    # панель юзера
    dp.callback_query.register(hide_faq_handler, F.data == "hide_faq")

    dp.callback_query.register(back, F.data == 'back')  # кнопка назад
    # dp.callback_query.register(back, F.data == 'farther')  # кнопка вперед

    return dp
