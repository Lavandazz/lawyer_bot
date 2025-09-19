from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.admin_keyboards import admin_kb
from keyboards.create_request import file_for_record
from keyboards.help_keyboard import help_kb, help_docs_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, CreateRequest, AnswerState, UserState, AdminMenuState
from utils.answers import documents_info
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
    bot_logger.debug(f'Начало обработки back. Текущее состояние: {current_state}')

    # возврат в главное меню
    if current_state in {MenuState.admin_menu, UserState.request}:
        await state.set_state(MenuState.main_menu)
        await call.message.edit_text(
            text=f"*Главное меню.*\n\n"
                 f"Кнопка - *Начать запрос* - переводит бота в режим принятия документов.\n"
                 f"Пожалуйста, перед началом работы, ознакомьтесь с инструкцией по команде /help.\n\n"
                 f"Ниже Вы можете зайти в личный кабинет, где отображаются все Ваши запросы.",
            reply_markup=await inline_menu_kb(call.from_user.id),
            parse_mode='Markdown'
        )

    # переход из документов и ответов в меню всех вопросов
    if current_state in {AnswerState.docs_questions, AnswerState. answer}:
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

    if current_state in {CreateRequest.wait_contract, CreateRequest.wait_acc_screenshot, CreateRequest.wait_pass,
                         CreateRequest.wait_ndfl, CreateRequest.wait_extract, CreateRequest.wait_record_book,
                         CreateRequest.wait_save, CreateRequest.wait_comment, CreateRequest.wait_surname}:
        await state.set_state(UserState.request)
        await call.message.edit_text(
            text="Выберите интересующий вопрос",
            reply_markup=file_for_record()
        )

    # переход в админ меню
    if current_state in {AdminMenuState.requests_menu, AdminMenuState.statistic_menu}:
        await state.set_state(MenuState.admin_menu)
        await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_kb())


async def clear_message(call: CallbackQuery, role: str):
    """ Скрыть уведомление о новом отзыве """
    if role == 'admin':
        await call.message.delete()
        bot_logger.debug(f'Удалил сообщение')
