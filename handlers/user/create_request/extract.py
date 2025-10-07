from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.cancel_state_handler import cancel_state_handler
from keyboards.back_keyboard import back_button
from keyboards.create_request import file_for_record
from states.menu_states import CreateRequest
from utils.config import bot
from utils.logging_config import bot_logger


async def creating_request_extract(call: CallbackQuery, state: FSMContext):
    """
    Загрузка выписки из индивидуального лицевого счета
    :param call: extract
    :param state: CreateRequest.wait_extract
    """
    await call.message.delete()
    data = await state.get_data()

    if not data.get("extract"):
        await call.message.answer(
            text=f"📎 Прикрепите выписку из индивидуального лицевого счета используя скрепку ниже.\n"
                 f"Для отмены нажмите на кнопку 'Назад' или команду /cancel",
            reply_markup=back_button()
        )
        await state.set_state(CreateRequest.wait_extract)
        await cancel_state_handler(user_id=call.from_user.id, bot=bot, state=state)
    else:
        await call.message.answer(
            text=f"Вы уже прикрепляли файл\n",
            reply_markup=back_button()
        )
    await state.set_state(CreateRequest.wait_extract)


async def creating_request_extract_save(message: Message, state: FSMContext):
    """
    Получение выписка из индивидуального лицевого счета.
    Ссылку file_id из телеграм сохраняем в state.data
    :param message: message.document/message.photo
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

    await state.update_data(extract=file_id)

    await message.answer(text=f"Файл ИЛС получен.\n"
                              f"Загрузите оставшиеся документы",
                         reply_markup=await file_for_record(state))
    await state.set_state(CreateRequest.save)

    bot_logger.info(f'Пользователь {message.from_user.id} загрузил ИЛС: '
                    f'{message.photo if message.photo else message.document.file_id}')

