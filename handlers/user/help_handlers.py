from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.back_keyboard import back_button
from keyboards.help_keyboard import help_kb, help_docs_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, AnswerState
from utils.answers import documents_info, answers_info


async def get_help(message: Message, bot: Bot, state: FSMContext):
    """
    Отображение клавиатуры по команде help
    """
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Выберите интересующий вопрос",
        reply_markup=help_kb()
    )
    await state.set_state(AnswerState.all_questions)


async def get_help_how_upload(call: CallbackQuery, state: FSMContext):
    """
    Ответ на вопросы, как загружать документы и как пользоваться ботом.
    """
    qu = call.data
    await call.message.edit_text(text=answers_info.get(qu),
                                 reply_markup=back_button(),
                                 parse_mode="Markdown"
    )
    await state.set_state(AnswerState.answer)


async def get_help_docs(call: CallbackQuery, state: FSMContext):
    """
    Отображение необходимых документов как кнопок.
    """
    await call.message.edit_text(
                           text=f"Какие документы нужны для расчета ⁉️",
                           reply_markup=help_docs_kb(documents_info),
                           parse_mode='Markdown')

    await state.set_state(AnswerState.docs_questions)


async def answer(call: CallbackQuery, state: FSMContext):
    """ Ответы на вопросы """
    for key, value in documents_info.items():
        if call.data == value[0]:  # Сравниваем call.data с [0]
            await call.message.edit_text(text=value[1], reply_markup=back_button())
            await state.set_state(AnswerState.doc_answer)


async def hide_faq_handler(call: CallbackQuery, state: FSMContext):
    """ Скрываем клавиатуру с вопросами """
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
        print(e)
        await call.answer("Не удалось скрыть", show_alert=True)

