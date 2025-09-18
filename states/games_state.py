from aiogram.fsm.state import StatesGroup, State


class GameMenuState(StatesGroup):
    """ Главное меню"""
    main_game_menu = State()
    upcoming_game_menu = State()
    past_game_menu = State()
    future_game = State()
    past_game = State()
    game = State()


class AddGameState(StatesGroup):
    main_add_menu = State()
    add_title = State()
    add_description = State()
    add_date = State()
    add_time = State()
    add_image = State()
    save_game = State()


