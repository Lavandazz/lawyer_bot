import os

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from database.config import RequestStatus
from keyboards.admin_keyboards import requests_kb
from keyboards.approval_keyboard import approve_request_kb
from keyboards.back_keyboard import back_button
from states.menu_states import AdminMenuState
from utils.config import bot
from utils.get_user import admin_only
from utils.logging_config import bot_logger
from services.requests import RequestService


@admin_only
async def show_requests(call: CallbackQuery, state: FSMContext, role: str):
    """
    Обработка кнопки Заявки на расчет.
    Получаем все SalaryRequest с prefetch_related - user (все запросы salary связанные с объектами user).
    requests передаем в клавиатуру.
    :param call: requests
    :param state: AdminMenuState.requests_menu
    :param role: admin
    :return:
    """

    requests = await RequestService.get_requests(status=RequestStatus.PENDING)
    if requests:
        await call.message.edit_text(text="Здесь отображены все заявки от пользователей",
                                     reply_markup=await requests_kb(requests, role))
    else:
        await call.message.edit_text(text="Заявок еще не было",
                                     reply_markup=back_button())
    await state.set_state(AdminMenuState.requests_menu)

    bot_logger.info(f"Меню заявок")


@admin_only
async def show_user_request(call: CallbackQuery, state: FSMContext, role: str):
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
        message_text = f"""📋 <b>Заявка №{request.id}</b>

        👤 <b>Пользователь:</b> {request.user.first_name} {request.user.second_name}
        📞 <b>Телефон:</b> {request.user.phone}
        ✉️ <b>Телеграм</b> @{request.user.username}
        📆 <b>Дата:</b> {request.created_at.strftime('%d.%m.%Y %H:%M')}
        💬 <b>Комментарий:</b> {request.comment if request.comment != "pass" else "Отсутствует"}
        📩  <b>Паспорт:</b> Отправлен на почту

        ✅ <b>Статус:</b> {RequestStatus.PENDING.value if RequestStatus.PENDING else 'на рассмотрении'}"""

        media_messages_ids = []  # список для медиа сообщений для удаления по кнопке Назад

        sent_message = await call.message.edit_text(
            text=message_text,
            parse_mode='HTML',  # меняем на HTML
            reply_markup=approve_request_kb(request_id=request.id, user_id=request.user.id))

        # media_messages_ids.append(sent_message.message_id)
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

        await state.set_state(AdminMenuState.request)

        bot_logger.info(f"Отображение заявки {request.id}")

    except Exception as e:
        bot_logger.exception(f"Ошибка в отображении заявки пользователя: {e}")
