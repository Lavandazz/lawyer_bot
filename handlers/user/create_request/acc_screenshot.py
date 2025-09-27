from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.cancel_state_handler import cancel_state_handler
from keyboards.back_keyboard import back_button
from keyboards.create_request import file_for_record
from states.menu_states import CreateRequest
from utils.config import bot
from utils.logging_config import bot_logger


async def creating_request_acc_screenshot(call: CallbackQuery, state: FSMContext):
    """
    Загрузка скриншота из ЛК ВБ
    :param call: acc_screenshot
    :param state: CreateRequest.wait_acc_screenshot
    """
    await call.message.delete()
    data = await state.get_data()

    bot_logger.debug(f"Current state data: {data}")
    bot_logger.debug(f"acc_screenshot in data: {data.get('acc_screenshot')}")

    if not data.get("acc_screenshot"):
        await call.message.answer(
            text=f"📎 Прикрепите скриншот из ЛК ВБ используя скрепку ниже..."
                 f"Формат JPEG.\n"
                 f"Для отмены нажмите на кнопку 'Назад' или команду /cancel",
            reply_markup=back_button()
        )
    else:
        await call.message.answer(
            text=f"Вы уже добавили скриншот\n",
            reply_markup=back_button()
        )
    await state.set_state(CreateRequest.wait_acc_screenshot)


async def creating_request_acc_screenshot_save(message: Message, state: FSMContext):
    """
    Получение и сохранение скрина из ЛК в формате PDF, PNG или JPEG.
    Ссылку file_id из телеграм сохраняем в state.data
    :param message: message.document / message.photo
    :param state: CreateRequest.save
    :return:
    """
    # Обработка фото (PNG, JPEG)
    bot_logger.debug("сохраняю скрин лк")

    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return

    await state.update_data(acc_screenshot=file_id)

    await message.answer(text=f"Скрин из ЛК получен\n"
                              f"Загрузите оставшиеся документы",
                         reply_markup=await file_for_record(state))
    await state.set_state(CreateRequest.save)
    bot_logger.debug(f'получен скрин: {message.document}, file_id: {file_id}')

