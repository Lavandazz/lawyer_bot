from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.barista_keyboard import barista_kb, barista_menu_kb, barista_game_menu_kb
from states.menu_states import BaristaState, AdminMenuState
from utils.get_user import staff_only
from utils.logging_config import bot_logger


@staff_only
async def barista_menu(call: CallbackQuery, state: FSMContext, role: str):
    """"""
    bot_logger.info('Вход в панель бариста')
    await call.message.edit_text('Выберите интересующий раздел)',
                                 reply_markup=barista_menu_kb())
    await state.set_state(BaristaState.menu)


@staff_only
async def show_barista_menu_game(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отображение меню игр
    """
    bot_logger.info('Бариста - меню игр')
    await state.set_state(BaristaState.games_menu)
    await call.message.edit_text(text='Вы находитесь в меню бариста.',
                                 reply_markup=barista_game_menu_kb())


@staff_only
async def show_barista_posts_menu(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отображение меню постов бариста
    """
    bot_logger.info('Бариста - меню постов')
    await state.set_state(BaristaState.posts_menu)
    await call.message.edit_text(text='Вы находитесь в меню бариста.',
                                 reply_markup=barista_kb())

