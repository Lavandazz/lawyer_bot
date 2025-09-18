from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.constants import TRANSITION_MAP
from utils.logging_config import bot_logger


class BackHandler:
    def __init__(self, call: CallbackQuery, state: FSMContext, role: str):
        self.call = call
        self.state = state
        self.role = role


    async def handle(self):
        """ Обработка кнопки 'Назад' """
        current_state = await self.state.get_state()
        bot_logger.debug(f'Текущее состояние: {current_state}')
        try:
            for now_state in TRANSITION_MAP.values():
                if current_state in now_state.get('states'):
                    await self.state.set_state(now_state.get('target_state'))
                    cur = await self.state.get_state()
                    mess, kb = await self.get_message(now_state)
                    print('mess, kb:', mess, kb)
                    await self.call.message.edit_text(text=mess,
                                                      reply_markup=kb)
                    bot_logger.debug(f'Новое состояние: {cur}')

        except Exception as e:
            bot_logger.exception(f'Ошибка state: {current_state}, {e}')

    @staticmethod
    async def get_message(now_state):
        text_state = now_state.get('text')
        kb = now_state.get('keyboard')
        return text_state, kb
