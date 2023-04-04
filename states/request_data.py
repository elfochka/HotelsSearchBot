from telebot.handler_backends import State, StatesGroup


class HighLowBest(StatesGroup):
    command = State()
    city = State()
    check_in = State()
    check_out = State()
    number_hotels = State()
    need_photo_yes_or_no = State()
    number_photos = State()
    result = State()
    finish = State()


class History(StatesGroup):
    select_search = State()
    selection_processing = State()


class Games(StatesGroup):
    games_list = State()
    game_select = State()


class TicTacToe(StatesGroup):
    start = State()
    gaming = State()
    finish = State()


class Blackjack(StatesGroup):
    start = State()
    gaming = State()
    finish = State()
