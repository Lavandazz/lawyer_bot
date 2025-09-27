from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.back_keyboard import back_button
from keyboards.help_keyboard import help_kb, help_docs_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, AnswerState
from utils.answers import documents_info, answers_info
from utils.config import bot
from utils.logging_config import bot_logger


async def get_help(message: Message, bot: Bot, state: FSMContext):
    """
    Команда /help.
    Отправляет клавиатуру с вопросами.
    :param message: /help
    :param bot: bot
    :param state: AnswerState.all_questions
    :return:
    """
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Выберите интересующий вопрос",
        reply_markup=help_kb()
    )
    await state.set_state(AnswerState.all_questions)


async def get_help_how_upload(call: CallbackQuery, state: FSMContext):
    """
    Ответы на вопросы, как загружать документы.
    :param call: how_upload
    :param state: AnswerState.answer
    :return:
    """
    qu = call.data
    await call.message.edit_text(text=answers_info.get(qu),
                                 reply_markup=back_button(),
                                 parse_mode="Markdown"
    )
    await state.set_state(AnswerState.answer)


async def get_help_docs(call: CallbackQuery, state: FSMContext):
    """
    Ответы на вопросы, какие загружать документы.
    :param call: what_upload
    :param state: AnswerState.docs_questions
    :return:
    """
    await call.message.edit_text(
                           text=f"Какие документы нужны для расчета ⁉️",
                           reply_markup=help_docs_kb(documents_info),
                           parse_mode='Markdown')

    await state.set_state(AnswerState.docs_questions)


async def hide_faq_handler(call: CallbackQuery, state: FSMContext):
    """
    Скрывает клавиатуру с вопросами по нажатию на кнопку - Скрыть.
    При неудаче бот отправляет клавиатуру главного меню.
    :param call: hide_faq
    :param state: MenuState.main_menu
    :return:
    """
    try:
        await call.message.edit_text(
            text=f"Главное меню.\n\n"
                 f"Кнопка - *Начать запрос* - переводит бота в режим принятия документов.\n"
                 f"Пожалуйста, перед началом работы, ознакомьтесь с инструкцией по команде /help.\n\n"
                 f"Ниже Вы можете зайти в личный кабинет, где отображаются все Ваши запросы.",
            reply_markup=await inline_menu_kb(call.from_user.id),
            parse_mode='Markdown'
        )
        await state.set_state(MenuState.main_menu)

    except Exception as e:
        bot_logger.exception(f"Не удалось скрыть клавиатуру с вопросами: {e}.\n"
                             f"Бот отправил главное меню.")
        await call.answer("Не удалось скрыть клавиатуру", show_alert=True)
        await bot.send_message(chat_id=call.from_user.id,
                               text="Главное меню",
                               reply_markup=await inline_menu_kb(call.from_user.id))


async def answer(call: CallbackQuery, state: FSMContext):
    """
    Ответы на вопросы о документах и где их взять.
    Сравниваем коллбеки со словарем call.data.
    :param call: get_
    :param state: AnswerState.doc_answer
    :return:
    """
    for key, value in documents_info.items():
        if call.data == value[0]:  # Сравниваем call.data с [0]
            await call.message.edit_text(text=value[1], reply_markup=back_button())
            await state.set_state(AnswerState.doc_answer)
