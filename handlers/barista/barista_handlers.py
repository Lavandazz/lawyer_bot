from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.back_keyboard import back_button
from keyboards.barista_keyboard import (get_review_keyboard, review_kb, get_post_keyboard,
                                        edit_text_keyboard, barista_posts_kb, barista_kb)
from states.menu_states import AdminMenuState, BaristaState, PostState
from database.models_db import AdminPost, User

from utils.get_user import is_admin
from utils.logging_config import bot_logger


@is_admin
async def add_admin_post(call: CallbackQuery, state: FSMContext, role: str):
    """
    Добавление поста админа
    :param call:
    :param state:
    :param role:
    :return:
    """
    await state.set_state(PostState.add_post)
    await call.message.edit_text('📤 Отправьте фото кофе с подписью (или просто фото)', reply_markup=back_button())


@is_admin
async def add_photo(message: Message, state: FSMContext, role: str):
    """
    Загрузка фото и текста публикации поста
    """
    bot_logger.debug(f'Жду фото поста. Состояние {await state.get_state()}')
    # await message.delete()
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фото!", reply_markup=back_button())
        return

    photo = message.photo[-1]  # Берём самое большое изображение
    text = message.caption  # Текст под фото (может быть None)

    await state.update_data(photo=photo, text=text)

    if not text:
        # Если текста нет, предлагаем ввести или генерируем автоматически
        await message.reply(
            "☕ Вы не добавили подпись. "
        )
        return
    else:
        # Если текст есть, сохраняем пост
        await message.answer('Выберите действие', reply_markup=edit_text_keyboard())


# @is_admin
# async def change_post(call: CallbackQuery, state: FSMContext, role: str):
#     """ Обработка кнопки для редактирования текста сгенерированного ии """
#     data = await state.get_data()
#     current_text = data.get('text', "Текст не найден")
#     await call.message.edit_text(
#         f"✏️ <b>Текущий текст:</b>\n\n{current_text}\n\n"
#         "Отправьте новый текст или нажмите 'Назад'",
#         reply_markup=back_button(),  # Кнопка для отмены
#         parse_mode="HTML"
#     )
#     await state.set_state(PostState.editing_text)  # Ждём новый текст


# @is_admin
# async def save_edited_text(message: Message, bot: Bot, state: FSMContext, role: str):
#     # Сохраняем новый текст в состоянии
#     # await state.set_state(PostState.save_post)
#     await state.update_data(text=message.text)
#     # Показываем обновлённый вариант
#     data = await state.get_data()
#     post_text = data.get("text")
#     post_photo = data.get('photo')
#     bot_logger.debug(f'1 Обновленный текст поста {post_text}')
#     bot_logger.debug(f'2 Обновленный текст поста {message.text}')
#
#     await bot.send_photo(
#         chat_id=message.chat.id,
#         photo=post_photo.file_id,
#         caption=f'✅ <b>Обновлённый текст:</b>\n\n{post_text}',
#         reply_markup=edit_text_keyboard(),
#         parse_mode="HTML"
#     )
#     await state.set_state(PostState.generated_text)  # Возвращаемся к состоянию подтверждения


@is_admin
async def save_post(call: CallbackQuery, state: FSMContext, bot: Bot, role: str):
    """ Загрузка файла и текста от бариста """
    post_data = await state.get_data()
    photo = post_data.get('photo')
    photo_file_id = photo.file_id
    text = post_data.get('text')

    if not text:
        await call.message.answer("Ошибка: текст не найдено!")
        return
    if not photo_file_id:
        await call.message.answer("Ошибка: фото не найдено!")
        return

    await state.set_state(PostState.save_post)
    # сохранение в бд
    post_id = await to_save(photo_file_id, text, call.from_user.id)

    await call.answer(text='Публикую пост')
    # публикация поста в канал
    # await publish_post_to_channel(bot=bot, photo_id=photo_file_id, text=text, post_id=post_id)

    await call.message.delete()
    await state.clear()

    await bot.send_message(chat_id=call.from_user.id, text='Возврат в меню', reply_markup=barista_kb())


async def to_save(photo: str, text: str, user_id: int):
    """ Сохранение поста бариста"""
    try:
        user = await User.get(telegram_id=user_id)
        post = await AdminPost.create(
            user_id=user,
            photo_file_id=photo,
            text=text
        )
        bot_logger.debug(f'Пост сохранен, {user.id} - {user.role}, пост - {post.id} ')
        return post.id
    except Exception as e:
        bot_logger.error(f'Ошибка сохранения поста, {e}')

@is_admin
async def moderate_review(call: CallbackQuery, bot: Bot, state: FSMContext, role: str):
    """ Обработка отзыва пользователя """
    await state.set_state(BaristaState.approve_menu)

    if not await is_admin(call.from_user.id):
        bot_logger.warning('недостаточно прав на модерацию отзыва')
        await call.answer("У вас нет прав на модерацию.")
        return

    review = await Review.get(id=call.data.split('_')[1])
    message = (f'Отзыв от {review.username}:\n\n'
               f'{review.text}')

    if not await state.get_state() == BaristaState.approve_menu.state:
        await call.message.delete()

    bot_logger.debug(await state.get_state())
    try:
        if review.photo_file_id:
            if await state.get_state() == BaristaState.approve_menu.state:
                await call.message.delete()
            bot_logger.info(f'Новый отзыв с фото')
            await bot.send_photo(chat_id=call.from_user.id, photo=review.photo_file_id,
                                 caption=message, reply_markup=get_review_keyboard(review.id))
        else:
            await call.message.edit_text(message, reply_markup=get_review_keyboard(review.id))

    except Exception as e:
        bot_logger.error(f'Ошибка в просмотре отзыва: {e}')


async def save_review(call: CallbackQuery, status: bool, role: str):
    """ Сохранение отзыва"""
    review_id = int(call.data.split("_")[1])
    review = await Review.get(id=review_id)
    user = await review.user
    telegram_id = user.telegram_id
    review.approved = status
    await review.save()
    return telegram_id


@is_admin
async def approve_review(call: CallbackQuery, bot: Bot, role: str, state: FSMContext):
    """ Одобрение отзыва """
    telegram_id = await save_review(call, True, role)  # получаем телеграм пользователя
    current_state = await state.get_state()
    print(f'Статус при одобрении {current_state}')
    await call.answer("Одобрено!")

    # if await state.get_state() == BaristaState.approve_menu:  # если отзыв отображается через меню бариста
    #     bot_logger.debug(f'Проверка статуса {current_state}')
    await state.set_state(BaristaState.review_menu)
    await bot.send_message(chat_id=call.from_user.id,
                           text="Вы находитесь в меню с отзывами клиентов",
                           reply_markup=await review_kb()
    )
    # пересылаем сообщение в канал
    await forward_review_to_channel(bot, call.from_user.id, call.message.message_id)

    await call.message.delete()
    await bot.send_message(chat_id=telegram_id, text='Ваш отзыв одобрен')


@is_admin
async def reject_review(call: CallbackQuery, bot: Bot, role: str, state: FSMContext):
    """ Отклонение отзыва """
    current_state = await state.get_state()
    telegram_id = await save_review(call, True, role)
    await call.answer("Отклонено!")

    await state.set_state(BaristaState.review_menu)
    # if await state.get_state() == BaristaState.approve_menu:
    await bot.send_message(chat_id=call.from_user.id,
                           text="Вы находитесь в меню с отзывами клиентов",
                           reply_markup=await review_kb()
                           )
    await call.message.delete()
    bot_logger.debug(f'новый статус после отклонения отзыва {await state.get_state()}')
    chat_id = telegram_id
    await bot.send_message(chat_id=telegram_id, text='Ваш отзыв отклонен')
    print('чат:', chat_id)


@is_admin
async def show_barista_posts(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение всех постов бариста как кнопки """
    await state.set_state(BaristaState.posts)
    bot_logger.debug(f'текущее состояние {await state.get_state()}')
    await call.message.edit_text(text=f'Выберите пост', reply_markup=await barista_posts_kb())


@is_admin
async def barista_post(call: CallbackQuery, state: FSMContext, bot: Bot, role: str):
    """ Отображение конкретного поста бариста """
    await state.set_state(BaristaState.post)
    bot_logger.debug(f'текущее состояние бариста {await state.get_state()}')
    post_id = call.data.split('_')[1]

    try:
        post = await AdminPost.get(id=post_id)
        await call.message.delete()  # удаляем клавиатуру, чтоб отобразить фото-пост

        await bot.send_photo(chat_id=call.message.chat.id,
                             photo=post.photo_file_id,
                             caption=post.text,
                             reply_markup=back_button())
    except Exception as e:
        bot_logger.warning(f'не удалось отправить сообщение с постом бариста: {e}')
