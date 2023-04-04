from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def ttt_board(field_cells: list) -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура-поле крестики-нолики
    :param field_cells:
    :return: (markup_inline) возвращает саму клавиатуру
    """
    board_buttons = [InlineKeyboardButton(
        text=field_cell[1], callback_data=field_cell[0]
    ) for field_cell in field_cells]
    markup_inline = InlineKeyboardMarkup(build_menu(board_buttons, n_cols=3))
    return markup_inline


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None) -> list:
    """
    построение кнопок для ttt_board
    :param buttons:
    :param n_cols:
    :param header_buttons:
    :param footer_buttons:
    :return:
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def ttt_yes_or_no() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура "да" или "нет"
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    item_yes = InlineKeyboardButton(text='Да', callback_data='y')
    item_no = InlineKeyboardButton(text='Нет', callback_data='n')
    markup_inline.add(item_yes, item_no)
    return markup_inline
