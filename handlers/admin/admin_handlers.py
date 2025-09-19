from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.models_db import SalaryRequest
from keyboards.admin_keyboards import admin_kb, requests_kb
from states.menu_states import AdminMenuState, MenuState
from utils.get_user import admin_only
from utils.logging_config import bot_logger


@admin_only
async def admin_menu(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение клавиатуры админ-панели """
    await state.set_state(MenuState.admin_menu)
    await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_kb())


@admin_only
async def admin_menu_requests(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение всех заявок """
    await state.set_state(AdminMenuState.requests_menu)
    requests = await SalaryRequest.all().prefetch_related('user_id')
    await call.message.edit_text(text="Здесь отображены все заявки от пользователей",
                                 reply_markup=await requests_kb(requests))

    await state.set_state(AdminMenuState.requests_menu)