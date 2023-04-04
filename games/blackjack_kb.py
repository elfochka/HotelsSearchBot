from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def bj_yes_or_no() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура "да" или "нет"
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    item_yes = InlineKeyboardButton(text='Да', callback_data='y')
    item_no = InlineKeyboardButton(text='Нет', callback_data='n')
    markup_inline.add(item_yes, item_no)
    return markup_inline


def bj_ore_or_stop() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура "еще" или "хватит"
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    item_yes = InlineKeyboardButton(text='Ещё', callback_data='m')
    item_no = InlineKeyboardButton(text='Хватит', callback_data='s')
    markup_inline.add(item_yes, item_no)
    return markup_inline
