import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.config import RequestStatus
from database.models_db import SalaryRequest
from handlers.admin.get_statistic_handlers import get_statistic
from handlers.message_texts import start_text
from handlers.user.user_lk_requests import user_lk
from keyboards.admin_keyboards import admin_kb, requests_kb, admin_stat_kb
from keyboards.create_request import file_for_record
from keyboards.help_keyboard import help_kb, help_docs_kb
from keyboards.menu_keyboard import inline_menu_kb
from services.requests import RequestService
from states.menu_states import MenuState, CreateRequest, AnswerState, UserState, AdminMenuState, ApproveState, \
    StatsState
from utils.answers import documents_info
from utils.config import bot
from utils.logging_config import bot_logger


async def back(call: CallbackQuery, state: FSMContext, bot: Bot, role: str):
    """
     Обработка кнопки 'Назад'.
     current_state - получаем текущее состояние из FSMContext и сравниваем с перечисленными состояниями
    :param call: CallbackQuery - необходим для изменения текста и клавиатуры
    :param state: Установка нового состояния
    :param bot: Глобальный экземпляр бота используется для отправки сообщения
    :param role:
    :return: text, kb
    """
    current_state = await state.get_state()
    # bot_logger.debug(f'Начало обработки back. Текущее состояние: {current_state}')

    # возврат в главное меню
    if current_state in {MenuState.admin_menu, UserState.all_requests}:
        await state.set_state(MenuState.main_menu)
        await call.message.edit_text(
            text=start_text,
            reply_markup=await inline_menu_kb(call.from_user.id),
            parse_mode='Markdown'
        )

    # переход из документов и ответов в меню всех вопросов
    if current_state in {AnswerState.docs_questions, AnswerState.answer}:
        await state.set_state(AnswerState.all_questions)
        await call.message.edit_text(
            text="Выберите интересующий вопрос",
            reply_markup=help_kb()
        )

    # переход из документа в меню вопросов о документах
    if current_state in {AnswerState.doc_answer}:
        await state.set_state(AnswerState.docs_questions)
        await call.message.edit_text(
            text="Выберите интересующий вопрос",
            reply_markup=help_docs_kb(documents_info)
        )

    # переход из добавления файлов в меню
    if current_state in {CreateRequest.wait_contract, CreateRequest.wait_acc_screenshot, CreateRequest.wait_personal_pass,
                         CreateRequest.wait_ndfl, CreateRequest.wait_extract, CreateRequest.wait_record_book,
                         CreateRequest.save, CreateRequest.wait_comment}:
        await state.set_state(UserState.all_requests)
        await call.message.edit_text(
            text="Выберите интересующий вопрос",
            reply_markup=await file_for_record(state)
        )

    # переход в админ меню
    if current_state in {AdminMenuState.requests_menu, AdminMenuState.statistic_menu}:
        await state.set_state(MenuState.admin_menu)
        await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_kb())

    # переход из запроса (через админа или пользователя) в меню заявок
    if current_state in {AdminMenuState.request, UserState.request, ApproveState.reject_comment}:
        await delete_messages('media_message_ids', call, state)
        # если странциа админа, то переход в админ панели заявок
        if current_state in {AdminMenuState.request, ApproveState.reject_comment}:

            requests = await RequestService.get_requests(status=RequestStatus.PENDING)
            await state.set_state(AdminMenuState.requests_menu)

            await call.message.edit_text(text='Заявки пользователей',
                                         reply_markup=await requests_kb(requests, role))
        # если не админ, то в личный кабинет юзера
        else:
            await user_lk(call, state)

    # переход из календаря статистики и очистка ожидания дат
    if current_state in {StatsState.waiting_date, StatsState.waiting_first_date,
                         StatsState.waiting_second_date, StatsState.answer}:
        await state.clear()
        bot_logger.debug(f"Очистил ожидание даты статистики")
        await call.message.edit_text(text="Выберите период", reply_markup=admin_stat_kb())
        await state.set_state(AdminMenuState.statistic_menu)


async def clear_message(call: CallbackQuery, role: str):
    """ Скрыть уведомление о новом отзыве """
    if role == 'admin':
        await call.message.delete()
        bot_logger.debug(f'Удалил сообщение')


async def delete_messages(state_message: str, call: CallbackQuery, state: FSMContext):
    """

    :param state_message: ключ из state data сообщений, которые нужно удалить
    :param call:
    :param state:
    :return:
    """
    data = await state.get_data()
    # Извлекаем список по ключу 'media_message_ids'
    message_ids = data.get(state_message, [])  # получаем список сообщений message_ids = [123, 124, 125, 126]
    bot_logger.debug(f"список сообщений для удаления: {state_message}")
    temp_msg = await call.message.answer("🔄 Ждите...")  # показываем сообщение пока идет удаление медиа

    if message_ids:
        try:
            # Параллельное удаление всех сообщений
            delete_tasks = [
                bot.delete_message(chat_id=call.from_user.id, message_id=msg_id)
                for msg_id in message_ids
            ]

            # Выполняем все задачи по удалению сообщений одновременно
            await asyncio.gather(*delete_tasks, return_exceptions=True)

            await temp_msg.delete()  # удаляем сообщение ожидания удаления

            # # Обрабатываем возможные ошибки
            # for i, result in enumerate(results):
            #     if isinstance(result, Exception):
            #         bot_logger.warning(f"Не удалось удалить сообщение {message_ids[i]}: {result}")

        except TelegramBadRequest as e:
            bot_logger.warning(f"Не удалось удалить сообщение {message_ids}: {e}")
            await state.set_state(MenuState.main_menu)
            await bot.send_message(text="Возврат в меню",
                                   chat_id=call.from_user.id,
                                   reply_markup=await inline_menu_kb(call.from_user.id))
