import random
from hotlog import hotels_log
from games.tic_tac_toe_kb import ttt_board, ttt_yes_or_no
from loader import bot
from states.request_data import TicTacToe


class Cell:
    #  Клетка, у которой есть значения
    #   - занята она или нет
    #   - номер клетки
    def __init__(self, x, y, value) -> None:
        """
        Инициализация клетки
        :param x:
        :param y:
        :param value:
        """
        self.x = x
        self.y = y
        self.value = value


class Board:
    #  Класс поля, который создаёт у себя экземпляры клетки
    def __init__(self) -> None:
        """
        Инициализация поля
        """
        self.cells = [[Cell(x, y, '-') for x in range(0, 3)
                       ] for y in range(0, 3)]

    def print_board(self) -> list:
        """
        Вывод поля
        :return:
        """
        field_cells = []
        for x in range(0, 3):
            for y in range(0, 3):
                field_cells.append([f'{x}-{y}', self.cells[x][y].value])
        return field_cells


class Player:
    #  У игрока может быть
    #   - имя
    #   - на какую клетку ходит
    def __init__(self, own_board, player_mark) -> None:
        """
        Инициализация игрока с привязанным к нему полем (с клетками)
        :param own_board:
        :param player_mark:
        """
        self.board = own_board
        self.mark = player_mark
        self.comp_mark = '0'

    def player_turn(self, coordinates) -> None:
        """
        Ход игрока
        :param coordinates:
        :return:
        """
        if self.board.cells[int(coordinates[0])][int(coordinates[1])].value \
                == '-':
            self.board.cells[int(coordinates[0])][int(coordinates[1])].value \
                = self.mark
            self.comp_turn()
        else:
            pass

    def comp_turn(self) -> None:
        """
        Ход компа
        :return:
        """
        while True:
            if self.is_game_end():
                break
            else:
                comp_x = random.randint(0, 2)
                comp_y = random.randint(0, 2)
                if self.board.cells[comp_x][comp_y].value == '-':
                    self.board.cells[comp_x][comp_y].value = self.comp_mark
                    break

    def is_game_end(self) -> str:
        """
        Проверка, что игра закончена. Кто-то выиграл или все ячейки заполнены
        :return:
        """
        for i in range(0, 2):
            if self.board.cells[i][0].value == self.board.cells[i][1].value \
                    == self.board.cells[i][2].value != '-':
                return self.board.cells[i][0].value
            elif self.board.cells[0][i].value == self.board.cells[1][i].value \
                    == self.board.cells[2][i].value != '-':
                return self.board.cells[0][i].value
        if self.board.cells[0][0].value == self.board.cells[1][1].value \
                == self.board.cells[2][2].value != '-':
            return self.board.cells[0][0].value
        elif self.board.cells[0][2].value == self.board.cells[1][1].value \
                == self.board.cells[2][0].value != '-':
            return self.board.cells[0][2].value
        elif self.board.cells[0][2].value == self.board.cells[1][2].value \
                == self.board.cells[2][2].value != '-':
            return self.board.cells[0][2].value

        is_nobody = True

        for x in range(0, 3):
            for y in range(0, 3):
                if self.board.cells[x][y].value == '-':
                    is_nobody = False

        if is_nobody:
            return '-'


# —————————————————————————
# |  0.0  |  0.1  |  0.2  |
# —————————————————————————
# |  1.0  |  1.1  |  1.2  |
# —————————————————————————
# |  2.0  |  2.1  |  2.2  |
# —————————————————————————

@bot.callback_query_handler(func=lambda call: True, state=TicTacToe.start)
def start_tic_tac_toe(call):
    try:
        mark = 'X'
        player = Player(Board(), mark)

        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            data['player'] = player
            data['mark'] = mark

        bot.send_message(call.from_user.id, 'Игра',
                         reply_markup=ttt_board(player.board.print_board()))
        bot.set_state(call.from_user.id, TicTacToe.gaming,
                      call.message.chat.id)
    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=TicTacToe.gaming)
def gaming_tic_tac_toe(call):
    try:
        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            player = data['player']
            mark = data['mark']

        player.player_turn(call.data.split('-'))

        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.id,
                                      reply_markup=ttt_board(
                                          player.board.print_board()
                                      ))
        bot.set_state(call.from_user.id, TicTacToe.gaming,
                      call.message.chat.id)

        if player.is_game_end():

            text = 'Игра закончена\n'
            if player.is_game_end() == mark:
                text += 'Вы выиграли!'
            elif player.is_game_end() == '-':
                text += 'Ничья'
            else:
                text += 'Вы проиграли!\n'

            text += '\nСыграем еще?'

            bot.send_message(call.from_user.id, text,
                             reply_markup=ttt_yes_or_no())
            bot.set_state(call.from_user.id, TicTacToe.finish,
                          call.message.chat.id)

    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True, state=TicTacToe.finish)
def finish_tic_tac_toe(call):
    try:
        bot.reset_data(call.from_user.id)

        if call.data == 'n':
            bot.set_state(call.from_user.id, None, call.message.chat.id)
        else:
            try:
                mark = 'X'
                player = Player(Board(), mark)

                with bot.retrieve_data(call.from_user.id,
                                       call.message.chat.id) as data:
                    data['player'] = player
                    data['mark'] = mark

                bot.send_message(call.from_user.id, 'Игра',
                                 reply_markup=ttt_board(
                                     player.board.print_board()))
                bot.set_state(call.from_user.id, TicTacToe.gaming,
                              call.message.chat.id)
            except Exception as e:
                hotels_log.logger.exception(e)
    except Exception as e:
        hotels_log.logger.exception(e)
