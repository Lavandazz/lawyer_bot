from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.back_keyboard import back_button
from keyboards.create_request import file_for_record
from services.file_manager import DocumentManager
from states.menu_states import CreateRequest
from utils.logging_config import bot_logger
from services.file_detector import FileDetector


async def creating_request_ndfl(call: CallbackQuery, state: FSMContext):
    """
    Загрузка файла 2-НДФЛ
    :param call: ndfl
    :param state: CreateRequest.wait_ndfl
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
    Ожидание 2-НДФЛ
    :param message: message.document / message.photo
    :param state: CreateRequest.save
    """

    doc = FileDetector(message)

    if not doc.is_file():
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return

    if doc.is_zip():
        await state.update_data(zip_ndfl=doc.file_id)
    else:
        await state.update_data(ndfl=doc.file_id)

    await message.answer(text=f"Файл 2-НДФЛ получен."
                              f"Загрузите оставшиеся документы\n",
                         reply_markup=await file_for_record(state))

    await state.set_state(CreateRequest.save)

    bot_logger.debug(f'получен НДФЛ: file_id: {doc.file_id}')



    # if message.document:
    #     file_id = message.document.file_id
    # # Обработка фото (PNG, JPEG)
    # elif message.photo:
    #     file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    # # elif message.document.file_name.endswith("zip"):