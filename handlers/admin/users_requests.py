from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from database.models_db import SalaryRequest
from keyboards.admin_keyboards import requests_kb
from keyboards.back_keyboard import back_button
from states.menu_states import AdminMenuState
from utils.config import bot
from utils.get_user import is_admin
from utils.logging_config import bot_logger


# @is_admin
async def show_requests(call: CallbackQuery, state: FSMContext, role: str):
    """
    Обработка кнопки Заявки на расчет
    """
    requests = await SalaryRequest.all().prefetch_related('user_id')
    # ДЕБАГ: Проверим какие пользователи действительно загружаются
    for i, request in enumerate(requests):
        print(f"Заявка {i+1}: ID={request.id}, User ID={request.user_id}, User={request.user_id},"
              f" Фамилия={request.user_id.second_name if request.user_id else 'None'}")
    if requests:
        await call.message.edit_text(text="Здесь отображены все заявки от пользователей",
                                     reply_markup=await requests_kb(requests))
        print(requests)
    else:
        await call.message.edit_text(text="Заявок еще не было",
                                     reply_markup=back_button())
    await state.set_state(AdminMenuState.requests_menu)


# @is_admin
async def show_user_request(call: CallbackQuery, state: FSMContext, role: str):
    """
    Обработка кнопки одного запроса на расчет
    """
    print(call.data)
    doc_id = call.data.split("_")[1]
    try:

        document = await SalaryRequest.filter(id=doc_id).prefetch_related('user_id').first()
        file_path = f"{document}"
        file_doc = FSInputFile(file_path)
        print(file_path)
        # message = (f"*Заявка от {document.user_id.second_name}:*"
        #            f"contract: {document.contract}")
        await bot.send_document(chat_id=call.from_user.id, caption=f"*Заявка от {document.user_id.second_name}:*",
                                document=file_doc)
        # await call.message.edit_text(text=message)
    except Exception as e:
        bot_logger.exception(e)
