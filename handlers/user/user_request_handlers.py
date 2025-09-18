from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.models_db import User, SalaryRequest
from handlers.cancel_state_handler import cancel_state_handler
from keyboards.back_keyboard import back_button, farther_and_back_button
from keyboards.create_request import file_for_record

from states.menu_states import CreateRequest, UserState
from utils.config import bot
from utils.logging_config import bot_logger


async def creating_request(call: CallbackQuery, state: FSMContext):
    """
    обработка кнопки 'добавить заявку'
    """
    await call.message.edit_text(text="Для загрузки документов, выберите кнопку",
                                 reply_markup=file_for_record())
    await state.set_state(UserState.request)

    # await call.message.edit_text(f"Прикрепите файл Договора ГПХ или трудовой договор.\n"
    #                              f"Допустимые форматы: .PNG, .PDF, .JPEG"
    #                              f"Для отмены введите команду /cancel\n"
    #                              f"Или нажмите на кнопку Назад",
    #                              input_field_placeholder="Нажмите на кнопку скрепки 📎",
    #                              reply_markup=back_button())
    # await state.set_state(CreateRequest.wait_contract)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=call.from_user.id, bot=bot, state=state)


async def creating_request_acc_screenshot(message: Message, state: FSMContext):
    """
    Получение файла с трудовым договором.
    Ожидание скрина из ЛК.
    """
    # Обработка документа (PDF, Word и т.д.)
    if message.document:
        print("трудовой", message.document.file_id, message.document.file_name)
        file_id = message.document.file_id
    # Обработка фото (PNG, JPEG)
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return

    await state.update_data(contract=file_id)

    bot_logger.debug(f'получен документ: {message.document}, file_id: {file_id}')

    await message.reply(text=f"Файл получен!\nТеперь прикрепите файл (скрин) из лк приложения ВБ Джоб.\n"
                             f"Для отмены введите команду /cancel\n"
                             f"Или нажмите на кнопку Назад"
                             f"Вы будете перенаправлены в главное меню",
                             input_field_placeholder="Нажмите на кнопку скрепки 📎",
                             reply_markup=back_button())
    await state.set_state(CreateRequest.wait_acc_screenshot)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


async def creating_request_pass(message: Message, state: FSMContext):
    """
    Получение скрина из ЛК.
    Ожидание фото бейджа
    """
    if not message.photo:
        await message.answer(text="Пожалуйста, прикрепите скрин из ЛК.\n"
                                  "Формат PNG, JPEG.")
        return

    file_id = message.photo[-1].file_id  # photo[-1].file_id
    bot_logger.debug(f'получен скрин лк: {message.photo}, file_id: {file_id}')

    await state.update_data(acc_screenshot=file_id)

    await message.reply(f"Прикрепите фото бейджа/пропуска \n"
                            f"Для отмены введите команду /cancel\n"
                            f"Или нажмите на кнопку Назад"
                            f"Вы будете перенаправлены в главное меню",
                            input_field_placeholder="Нажмите на кнопку скрепки 📎",
                            reply_markup=back_button())

    await state.set_state(CreateRequest.wait_pass)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


async def creating_request_ndfl(message: Message, state: FSMContext):
    """
    Получение скрина из ЛК.
    Ожидание ндфл
    """
    if not message.photo:
        await message.answer(text="Пожалуйста, фото бейджа/пропуска.\n"
                                  "Формат PNG, JPEG.")
        return
    file_id = message.photo[-1].file_id  # photo[-1].file_id
    bot_logger.debug(f'получено фото бейджа/пропуска: {message.photo}, file_id: {file_id}')

    await state.update_data(a_pass=file_id)

    await message.reply(f"Прикрепите файл 2 НДФЛ\n"
                            f"Для отмены введите команду /cancel\n"
                            f"Или нажмите на кнопку Назад"
                            f"Вы будете перенаправлены в главное меню",
                            input_field_placeholder="Нажмите на скрепку 📎",
                            reply_markup=back_button())

    await state.set_state(CreateRequest.wait_ndfl)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


async def creating_request_extract(message: Message, state: FSMContext):
    """
    Получение ндфл.
    Ожидание выписки из индивидуального лицевого счета
    """
    if message.document:
        file_id = message.document.file_id
    # Обработка фото (PNG, JPEG)
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return

    bot_logger.debug(f'Получен скрин НДФЛ: file_id: {file_id}')

    await state.update_data(ndfl=file_id)

    await message.reply(f"Прикрепите выписку из индивидуального лицевого счета\n"
                            f"Для отмены введите команду /cancel\n"
                            f"Или нажмите на кнопку Назад"
                            f"Вы будете перенаправлены в главное меню",
                            input_field_placeholder="Нажмите на кнопку скрепки 📎",
                            reply_markup=back_button())

    await state.set_state(CreateRequest.wait_extract)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


async def creating_request_record(message: Message, state: FSMContext):
    """
    Получение выписки из индивидуального лицевого счета.
    Ожидание трудовая книжка
    """
    if message.document:
        file_id = message.document.file_id
    # Обработка фото (PNG, JPEG)
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return
    bot_logger.debug(f'Получена выписка : {message.document}, file_id: {file_id}')

    await state.update_data(extract=file_id)

    await message.reply(f"Прикрепите трудовую книжку\n"
                            f"Для отмены введите команду /cancel\n"
                            f"Или нажмите на кнопку Назад"
                            f"Вы будете перенаправлены в главное меню",
                            input_field_placeholder="Нажмите на кнопку скрепки 📎",
                            reply_markup=back_button())

    await state.set_state(CreateRequest.wait_record)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


async def creating_request_comment(message: Message, state: FSMContext):
    """
    Получение трудовой книжки.
    Ожидание комментария.
    """
    if message.document:
        file_id = message.document.file_id
    # Обработка фото (PNG, JPEG)
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото наивысшего качества
    else:
        await message.answer("Пожалуйста, отправьте файл в формате PDF, PNG или JPEG")
        return
    bot_logger.debug(f'получена трудовая книжка: {message.document}, file_id: {file_id}')

    await state.update_data(record=file_id)

    await message.reply(f"Здесь Вы можете написать свой комментарий. ☕\n"
                            f"Для отмены введите команду /cancel\n"
                            f"Или нажмите на кнопку Назад\n"
                            f"Вы будете перенаправлены в главное меню",
                            reply_markup=farther_and_back_button())

    await state.set_state(CreateRequest.wait_comment)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


async def creating_request_message(message: Message, state: FSMContext):
    """
    Если был передан комментарий, сохраняем его в data.
    Далее обрабатываются все данные из data и сохраняются.
    """
    await state.update_data(comment=message.text, telegram=message.from_user.id)
    await creating_request_save(state=state)

    await message.edit_text(
        text="Данные отправлены на проверку",
        reply_markup=back_button()
    )
    await state.set_state(CreateRequest.wait_save)

    # автоматический сброс состояния через 10 минут
    await cancel_state_handler(user_id=message.from_user.id, bot=bot, state=state)


async def creating_request_call(call: CallbackQuery, state: FSMContext):
    """
    Если пользователь не оставляет комментарий, то используется кнопка Далее,
    сохраняем comment в data как строку pass
    Далее обрабатываются все данные из data и сохраняются.
    """
    print('Была нажата кнопка далее', call.data)
    if call.data == "farther":
        # сохраняем comment и telegram
        await state.update_data(comment="pass", telegram=call.from_user.id)
        await creating_request_save(state=state)
    await call.message.edit_text(
        text="Данные отправлены на проверку",
        reply_markup=back_button()
    )
    await state.set_state(CreateRequest.wait_save)


async def creating_request_save(state: FSMContext):
    """
    Получение всех документов из data, сохранение в бд
    :param state:
    :return:
    """

    docs = await state.get_data()
    contract = docs.get('contract')
    screenshot = docs.get('acc_screenshot')
    a_pass = docs.get('a_pass')
    extract = docs.get('extract')
    ndfl = docs.get('ndfl')
    record = docs.get('record')
    comment = docs.get('comment')
    telegram = docs.get('telegram')

    user = await User.get(telegram_id=telegram)

    try:
        await SalaryRequest.create(
            user_id=user.id,
            contract=contract,
            screenshot=screenshot,
            a_pas =a_pass,
            extract=extract,
            ndfl=ndfl,
            record=record,
            comment=comment
        )
        await state.clear()
    except Exception as e:
        bot_logger.exception(f"Не получилось сохранить заявку: {e}")


    # sender = SendMessage(user_role='barista', user=user, bot=bot, review_id=review.id, text=caption, file_id=file_id)
    # await sender.send_message()

    # await message.answer(text="Спасибо за отзыв с фото! Бариста его рассмотрит ☕",
    #                      reply_markup=await inline_menu_kb(message.from_user.id))



# async def handle_review_text(message: Message, state: FSMContext, bot: Bot):
#     """ Загрузка текстового отзыва от пользователя """
#     user = await User.get(telegram_id=message.from_user.id)
#     review = await Review.create(
#         user=user,
#         username=message.from_user.username,
#         first_name=message.from_user.first_name,
#         text=message.text
#     )
#
#     sender = SendMessage(user_role='barista', user=user, bot=bot, review_id=review.id, text=message.text)
#     await sender.send_message()
#     await message.answer(text="Спасибо за отзыв! Бариста его рассмотрит ☕",
#                          reply_markup=await inline_menu_kb(message.from_user.id))
#     await state.clear()
