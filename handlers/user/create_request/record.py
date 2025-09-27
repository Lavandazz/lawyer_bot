from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.back_keyboard import back_button
from keyboards.create_request import file_for_record
from states.menu_states import CreateRequest

from utils.logging_config import bot_logger


async def creating_request_record_book(call: CallbackQuery, state: FSMContext):
    """
    Загрузка файла электронной трудовой книжки
    :param call: pass
    :param state: CreateRequest.wait_record_book
    """
    await call.message.delete()
    data = await state.get_data()

    if not data.get("record_book"):
        await call.message.answer(
            text=f"📎 Прикрепите трудовую книжку используя скрепку ниже.\n"
                 f"Для отмены нажмите на кнопку 'Назад' или команду /cancel",
            reply_markup=back_button()
        )
    else:
        await call.message.answer(
            text=f"Вы уже прикрепляли скриншот\n",
            reply_markup=back_button()
        )
    await state.set_state(CreateRequest.wait_record_book)


async def creating_request_record_book_save(message: Message, state: FSMContext):
    """
    Получение электронной трудовой книжки.
    Ссылку file_id из телеграм сохраняем в state.data
    :param message: message.document / message.photo
    :param state: CreateRequest.save
    :return:
    """
    if message.document:
        file_id = message.document.file_id
    # Обработка фото (PNG, JPEG)
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return

    await state.update_data(record_book=file_id)

    await message.answer(text=f"Фото получено.\n"
                              f"Загрузите оставшиеся документы",
                         reply_markup=await file_for_record(state))
    await state.set_state(CreateRequest.save)

    bot_logger.debug(f'получен трудовой книжки: {message.photo}, file_id: {file_id}')
