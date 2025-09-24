from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.cancel_state_handler import cancel_state_handler
from keyboards.back_keyboard import back_button
from keyboards.create_request import file_for_record
from states.menu_states import CreateRequest
from utils.config import bot
from utils.logging_config import bot_logger


async def creating_request_ndfl(call: CallbackQuery, state: FSMContext):
    """
    Загрузка трудового договора
    :param call: ndfl
    :param state: wait_ndfl
    """
    await call.message.delete()
    data = await state.get_data()

    if not data.get("ndfl"):
        await call.message.answer(
            text=f"📎 Прикрепите файд 2-НДФЛ используя скрепку ниже.\n"
                 f"Для отмены нажмите на кнопку 'Назад' или команду /cancel",
            reply_markup=back_button()
        )
    else:
        await call.message.answer(
            text=f"Вы уже прикрепляли файл\n",
            reply_markup=back_button()
        )
    await state.set_state(CreateRequest.wait_ndfl)


async def creating_request_ndfl_save(message: Message, state: FSMContext):
    """
    Получение скрина из ЛК.
    Ожидание фото бейджа
    """
    if message.document:
        file_id = message.document.file_id
    # Обработка фото (PNG, JPEG)
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return

    await state.update_data(ndfl=file_id)

    await message.answer(text=f"Файл 2-НДФЛ получен."
                              f"Загрузите оставшиеся документы\n",
                         reply_markup=await file_for_record(state))
    await state.set_state(CreateRequest.save)

    bot_logger.debug(f'получен НДФЛ: file_id: {file_id}')

