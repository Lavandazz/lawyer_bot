from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.admin_keyboards import admin_kb
from states.menu_states import MenuState
from utils.get_user import admin_only



@admin_only
async def admin_menu(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение клавиатуры админ-панели """
    await state.set_state(MenuState.admin_menu)
    await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_kb())


