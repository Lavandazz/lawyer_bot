import asyncio
import logging
import time
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.menu_keyboard import inline_menu_kb
from utils.logging_config import bot_logger


async def cancel_handler(message: Message, bot: Bot, state: FSMContext):
    """ Сброс состояния ввода данных """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    bot_logger.info(f"Состояние ожидания: {current_state} - отменено")
    await asyncio.sleep(0.3)
    await message.answer(f"Действие отменено.\n"
                         f"Возврат в главное меню",
                         reply_markup=await inline_menu_kb(message.from_user.id))


async def cancel_state_handler(user_id: int, bot: Bot, state: FSMContext):
    """ Автоматический сброс состояния """
    try:
        current_state = await state.get_state()
        if not current_state:
            # Если состояния нет, ничего не делаем
            return
        await asyncio.sleep(600)
        new_current_state = await state.get_state()
        if current_state == new_current_state:
            # user_id = user_id
            await bot.send_message(user_id, 'Ожидание ввода превышено.\n Отмена сохранения данных.\n\n'
                                            'Вы возвращены в главное меню.',
                                   reply_markup=await inline_menu_kb(user_id))
            await state.clear()
            bot_logger.info(f'Состояние сброшено: {current_state} ')

    except Exception as e:
        bot_logger.warning(f"Ошибка в cancel_state_handler: {e}")
