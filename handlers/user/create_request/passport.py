from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.approval_keyboard import yes_or_no_btn, approve
from keyboards.back_keyboard import back_button
from keyboards.create_request import file_for_record
from states.menu_states import CreateRequest

from utils.logging_config import bot_logger


async def creating_request_passport(call: CallbackQuery, state: FSMContext):
    """
    Уведомление о необходимости выслать паспорт на почту.
    :param call: comment
    :param state: CreateRequest.wait_comment
    :return:
    """
    data = await state.get_data()
    if not data.get("passport"):
        await call.message.edit_text(
            text="Для оформления документов нам необходима копия вашего паспорта.\n"
                 "Пожалуйста, подтвердите, что вы уже отправили скан-копии на почту нашему юристу.\n\n"
                 "📧 E-mail: daria-chuprinina@mail.ru\n"
                 "(первая страница и страница с регистрацией)\n\n"
                 "Это обязательный шаг для продолжения работы.",
            reply_markup=approve())
    else:
        await call.message.edit_text(
            text=f"*Вы уже отвечали на запрос:*\n"
                 f"{data['comment']}\n",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button()
        )

    await state.set_state(CreateRequest.wait_passport)


async def creating_request_passport_save(call: CallbackQuery, state: FSMContext):
    """
    Если был нажата кнопка Да, сохраняем ответ в state data.
    Если нет, отображается клавиатура со всеми документами
    Далее обрабатываются все данные из data и сохраняются.
    Ссылку file_id из телеграм сохраняем в state.data
    :param message: approve_yes/approve_no
    :param state: CreateRequest.save
    """
    if call.data == "yes":
        await state.update_data(passport=True)

        await call.message.edit_text(
            text=f"Ответ учтен.\n",
            reply_markup=await file_for_record(state)
        )
        await state.set_state(CreateRequest.save)
        bot_logger.info(f'Пользователь {call.from_user.id} добавил ответ о паспорте')

    if call.data == "no":
        await call.message.edit_text(
            text="Выберите документ для отправки",
            reply_markup=await file_for_record(state)
        )



