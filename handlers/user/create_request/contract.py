from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.cancel_state_handler import cancel_state_handler
from keyboards.back_keyboard import back_button
from keyboards.create_request import file_for_record
from states.menu_states import CreateRequest
from utils.config import bot
from utils.logging_config import bot_logger


async def creating_contract(call: CallbackQuery, state: FSMContext):
    """
    Загрузка трудового договора
    :param call: contract
    :param state: wait_contract
    """
    await call.message.delete()
    data = await state.get_data()

    bot_logger.debug(f"Current state data: {data}")
    bot_logger.debug(f"contract in data: {data.get('acc_screenshot')}")

    if not data.get("contract"):
        await call.message.answer(
            text=f"📎 Прикрепите файл с трудовым договором/ГПХ используя скрепку ниже."
                 f"Формат файла PDF.\n"
                 f"Для отмены нажмите на кнопку 'Назад' или команду /cancel",
            reply_markup=back_button()
        )
    else:
        await call.message.answer(
            text=f"Вы уже добавили договор\n"
                 f"Загрузите оставшиеся документы",
            reply_markup=back_button()
        )
    await state.set_state(CreateRequest.wait_contract)


async def creating_contract_save(message: Message, state: FSMContext):
    """
    Получение файла с трудовым договором.
    """
    # Обработка документа (PDF, Word и т.д.)
    if message.document:
        file_id = message.document.file_id
    # Обработка фото (PNG, JPEG)
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return

    await state.update_data(contract=file_id)
    await message.answer(text=f"Договор получен\n"
                              f"Загрузите оставшиеся документы",
                         reply_markup=await file_for_record(state))
    await state.set_state(CreateRequest.save)