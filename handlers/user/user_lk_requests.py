import os

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from keyboards.admin_keyboards import requests_kb
from keyboards.back_keyboard import back_button
from services.requests import RequestService
from states.menu_states import UserState
from utils.config import bot
from utils.logging_config import bot_logger


async def user_lk(call: CallbackQuery, state: FSMContext):
    """
    Переход в личный кабинет пользователя, где отображаются заявки.
    :param call: my_requests
    :param state: UserState.all_requests
    :return:
    """
    await state.set_state(UserState.all_requests)
    try:

        requests = await RequestService.get_user_requests_by_id(telegram_id=call.from_user.id)
        await call.message.edit_text(
            text="Мои заявки",
            reply_markup=await requests_kb(requests, role="user"))

    except Exception as e:
        bot_logger.exception(e)


async def show_my_request(call: CallbackQuery, state: FSMContext):
    """
    Отображение информации о заявке по клику на кнопку с ФИО.
    :param call: request_{request.id}
    :param state: AdminMenuState.request
    :param role: admin
    :return:
    """
    request_id = call.data.split("_")[2]
    try:

        request = await RequestService.get_user_request(request_id=request_id)
        if not request:
            await call.answer("Заявка не найдена")
            return

        photos = []
        documents = []

        files_mapping = {
            "Договор ГПХ/трудовой": request.contract,
            "Скрин ЛК ВБ Джоб": request.account_screenshot,
            "Пропуск/Бейдж": request.a_pass,
            "Справка НДФЛ": request.ndfl_reference,
            "Выписка ИЛС": request.extract,
            "Электронная трудовая книжка": request.employment_record
        }

        for file_type, filename in files_mapping.items():
            if filename:
                file_path = filename
                if os.path.exists(file_path):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                        photos.append((file_type, filename, file_path))
                    else:
                        documents.append((file_type, filename, file_path))

        # 1. Отправляем основную информацию с кнопками
        message_text = f"""📋 *Заявка №{request.id}*

        👤 *Пользователь:* {request.user.first_name} {request.user.second_name}
        📅 *Дата:* {request.created_at.strftime('%d.%m.%Y %H:%M')}
        💬 *Комментарий:* {"Комментария нет" if request.comment == 'pass' else request.comment}
        
        {request.reject_comment if request.reject_comment else ""}
        
        *Статус:* {'✅ Одобрена' if request.status == 1 else '❌ Отклонена' if request.status == 2 else '⏳ На рассмотрении'}"""

        media_messages_ids = []  # список для медиа сообщений для удаления по кнопке Назад

        sent_message = await call.message.edit_text(
            text=message_text,
            parse_mode='MarkdownV2')

        media_messages_ids.append(sent_message.message_id)
        # 2. Отправляем файлы
        if photos:
            media_group = []
            for file_type, filename, file_path in photos:
                # объединяем все фото файлы в одну медиа группу
                media_group.append(InputMediaPhoto(media=FSInputFile(file_path)))

            sent_message = await bot.send_media_group(chat_id=call.from_user.id,
                                                      media=media_group)
            media_messages_ids.extend([msg.message_id for msg in sent_message])  # Добавляем каждый ID в список

        if documents:
            for file_type, filename, file_path in documents:

                sent_message = await bot.send_document(
                    chat_id=call.from_user.id,
                    document=FSInputFile(file_path)
                )
                media_messages_ids.append(sent_message.message_id)  # Добавляем каждый ID в список

        await state.update_data(media_message_ids=media_messages_ids)  # сохраняем ключ в data

        await bot.send_message(chat_id=call.from_user.id, text="Для возврата в меню нажмите на кнопку ниже",
                               reply_markup=back_button())

        await state.set_state(UserState.request)

    except Exception as e:
        bot_logger.exception(f"Ошибка в отображении заявки пользователя: {e}")
