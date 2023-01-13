from telebot.handler_backends import State, StatesGroup


class UserSearchParam(StatesGroup):
    city = State()
    number_hotels = State()
    need_photo_yes_or_no = State()
    number_photos = State()
