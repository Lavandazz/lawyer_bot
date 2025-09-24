import os

from keyboards.menu_keyboard import inline_menu_kb
from utils.config import bot, SUPERADMIN
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.models_db import User, SalaryRequest

from keyboards.create_request import file_for_record

from states.menu_states import UserState
from utils.config import bot, CLIENTS_DIR
from utils.logging_config import bot_logger
from utils.save_docs import get_docs_from_state, create_folder, save_all_docs
from utils.send_messages import SendMessage

if not os.path.exists(CLIENTS_DIR):
    os.makedirs(CLIENTS_DIR, exist_ok=True)


async def creating_request(call: CallbackQuery, state: FSMContext):
    """
    обработка кнопки 'добавить заявку'
    """
    await call.message.edit_text(text="Для загрузки документов, выберите кнопку",
                                 reply_markup=await file_for_record(state))

    await state.set_state(UserState.request)


async def creating_request_save(call: CallbackQuery, state: FSMContext):
    """
    Получение всех документов из data, сохранение в бд
    :param state:
    :return:
    """
    bot_logger.debug('Получаю все data state')

    # Получаем документы из state
    docs_data = await get_docs_from_state(state)
    docs = docs_data['docs']
    missing_docs = docs_data['missing']

    # Проверяем, все ли документы загружены
    if not docs_data['is_complete']:
        missing_list = "\n".join([f"• {doc}" for doc in missing_docs])
        bot_logger.info(f' Не все документы загружены. {missing_list} ')
        await call.message.edit_text(
            text=f"❌ Не все документы загружены!\n\nОтсутствуют:\n{missing_list}\n\n"
                 f"Пожалуйста, загрузите недостающие документы.",
            reply_markup=await file_for_record(state)
        )
        return

    try:
        user = await User.get(telegram_id=call.from_user.id)
        user_folder = f"{user.second_name}_{user.first_name[0]}_{user.patronymic[0]}"
        # Создаем папку для пользователя
        folder_path = create_folder(user_folder)
        # Сохраняем файлы и получаем пути
        file_paths = await save_all_docs(bot, folder_path, docs)
        # Сохраняем заявку в БД
        request = await SalaryRequest.create(
            user=user,  # передаем весь объект
            contract=file_paths.get('contract'),
            account_screenshot=file_paths.get('acc_screenshot'),
            a_pass=file_paths.get('personal_pass'),
            extract=file_paths.get('extract'),
            ndfl_reference=file_paths.get('ndfl'),
            employment_record=file_paths.get('record_book'),
            comment=docs['comment']
        )
        bot_logger.info(f"Новый запрос по отпускным")
        await state.clear()

        sender = SendMessage(user_role='admin', user=user, bot=bot, salary_request=request.id, text=request.comment)
        await sender.send_message()

        await call.message.answer(text="Обращение принято! Юрист его рассмотрит в ближайшее время ✉️",
                                  reply_markup=await inline_menu_kb(call.from_user.id))

        # await bot.send_message(chat_id=SUPERADMIN, text="новый запрос")

    except Exception or AttributeError as e:
        bot_logger.exception(f"Не получилось сохранить заявку: {e}")
        await bot.send_message(chat_id=call.from_user.id, text="Не удалось отправить заявку. Попробуйте позже.",
                               reply_markup=await inline_menu_kb(call.from_user.id))


