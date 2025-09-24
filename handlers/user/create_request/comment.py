from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.user.user_request_handlers import creating_request_save
from keyboards.back_keyboard import back_button, farther_and_back_button
from keyboards.create_request import file_for_record
from states.menu_states import CreateRequest

from utils.logging_config import bot_logger


async def creating_request_comment(call: CallbackQuery, state: FSMContext):
    """
    Ожидание комментария.
    """
    data = await state.get_data()
    if not data.get("comment"):
        await call.message.edit_text(f"Здесь Вы можете написать свой комментарий. ☕\n"
                                          f"Для отмены введите команду /cancel\n"
                                          f"Или нажмите на кнопку Назад\n"
                                          f"Вы будете перенаправлены в главное меню.",
                                          reply_markup=back_button())
    else:
        await call.message.answer(
            text=f"*Вы уже оставили комментарий к запросу:*\n"
                 f"{data['comment']}\n",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button()
        )

    await state.set_state(CreateRequest.wait_comment)


async def creating_request_comment_save(message: Message, state: FSMContext):
    """
    Если был передан комментарий, сохраняем его в data.
    Далее обрабатываются все данные из data и сохраняются.
    """
    await state.update_data(comment=message.text, telegram=message.from_user.id)

    await message.answer(
        text=f"Комментарий учтен.\n"
             f"Загрузите оставшиеся документы",
        reply_markup=await file_for_record(state)
    )
    await state.set_state(CreateRequest.save)

