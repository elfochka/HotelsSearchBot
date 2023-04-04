from games.blackjack import start_blackjack
from games.tic_tac_toe import start_tic_tac_toe
from hotlog import hotels_log
from keyboards.inline.keyboard import game_select
from loader import bot
from states.request_data import Games


@bot.message_handler(commands=['games'])
def get_games(message) -> None:
    """
    ловим команду 'games'
    Запрашиваем город у пользователя и записываем команду
    :param message: сообщение пользователя
    :return: (None)
    """
    bot.set_state(message.from_user.id, Games.games_list, message.chat.id)
    try:
        text = 'Во что сыграем?'
        bot.send_message(message.from_user.id, text,
                         reply_markup=game_select())
        bot.set_state(message.from_user.id, Games.game_select, message.chat.id)
    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=Games.game_select)
def select_game(call) -> None:
    """
    Выбор игры
    :param call:
    :return:
    """
    if int(call.data) == 1:
        start_tic_tac_toe(call)
    elif int(call.data) == 2:
        start_blackjack(call)
