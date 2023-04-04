from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_yes_or_no() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура "да" или "нет"
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    item_yes = InlineKeyboardButton(text='Да', callback_data='Да')
    item_no = InlineKeyboardButton(text='Нет', callback_data='Нет')
    markup_inline.add(item_yes, item_no)
    return markup_inline


def inline_numbers(max_num) -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура с числами от 1
    :param max_num: максимальное число
    :return: (markup_inline) возвращает саму клавиатуру
    """
    num_list = [InlineKeyboardButton(text=i, callback_data=i)
                for i in range(1, max_num + 1)]
    markup_inline = InlineKeyboardMarkup(build_menu(num_list, n_cols=5))
    return markup_inline


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None) -> list:
    """
    Меню для inline_numbers клавиатуры
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


def game_select() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура выбор игры
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    item_1 = InlineKeyboardButton(text='Крестики-нолики',
                                  callback_data=1)
    item_2 = InlineKeyboardButton(text='Блэк джек',
                                  callback_data=2)

    markup_inline.add(item_1, item_2)
    return markup_inline


def hotels_history(history_output_text) -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура с выводом истории поиска
    :param history_output_text:
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()

    for key, value in history_output_text.items():
        button_text = value

        markup_inline.add(InlineKeyboardButton(text=button_text,
                                               callback_data=key), )
    return markup_inline
