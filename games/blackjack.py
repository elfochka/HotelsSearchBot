import random

from games.blackjack_kb import bj_yes_or_no, bj_ore_or_stop
from hotlog import hotels_log
from loader import bot
from states.request_data import Blackjack


class Card:
    def __init__(self, name, suit, value) -> None:
        """
        Инициализация одной карты
        :param name:
        :param suit:
        :param value:
        """
        self.name = name
        self.suit = suit
        self.value = value


class Deck:
    # *Формирование новой колоды*
    # Карты имеют такие «ценовые» значения:
    # от двойки до десятки — от 2 до 10 соответственно;
    # у туза — 1 или 11 (11 пока общая сумма не больше 21, далее 1);
    # у «картинок» (король, дама, валет) — 10.
    def __init__(self) -> None:
        """
        Инициализация колоды
        """
        values_simple = ['двойка', 'тройка', 'четвёрка', 'пятёрка', 'шестёрка',
                         'семёрка', 'восьмёрка', 'девятка',
                         'десятка']
        values_picture = ['валет', 'дама', 'король']
        deck_suits = ['черви', 'пики', 'трефы', 'бубны']

        self.cards = ([Card(values_simple[k - 2], deck_suits[i], k) for k in
                       range(2, 11) for i in range(0, 4)] +
                      [Card(values_picture[k], deck_suits[i], 10) for k in
                       range(0, 3) for i in range(0, 4)] +
                      [Card('туз', deck_suits[i], 11) for i in range(0, 4)])
        random.shuffle(self.cards)

    def cards_print(self):
        i = 1
        cards = 'Карты: '
        for card in self.cards:
            output = str(i) + '. ' + str(card.name) + ' ' + str(card.suit) + \
                     ' ' + str(card.value)
            i += 1
            cards += output + ', '
        return cards


class Player:
    def __init__(self, own_deck):
        self.sum = 0
        self.deck = own_deck
        self.hand = []
        self.computer_hand = []
        self.computer_sum = 0

        for _ in range(0, 2):
            player_card = self.deck.cards.pop(0)
            self.hand.append(player_card)
            if player_card.name == 'туз':
                if self.sum >= 21:
                    player_card.value = 1
            self.sum += player_card.value

            computer_card = self.deck.cards.pop(0)
            self.computer_hand.append(computer_card)
            if computer_card.name == 'туз':
                if self.sum >= 21:
                    computer_card.value = 1
            self.computer_sum += computer_card.value

    def take_card(self):
        player_card = self.deck.cards.pop(0)
        self.hand.append(player_card)
        if player_card.name == 'туз':
            if self.sum >= 21:
                player_card.value = 1
        self.sum += player_card.value

    def hand_print(self):
        text = f'Карты у Вас на руках, Очков: {self.sum}'
        i = 1
        for card in self.hand:
            output = str(i) + '. ' + str(card.name) + ' ' + str(card.suit) + \
                     ' ' + str(card.value)
            i += 1
            text += '\n' + output
        return text

    def computer_hand_print(self):
        text = f'Карты на руках у компьютера, Очков: {self.computer_sum}'
        i = 1
        for card in self.computer_hand:
            output = str(i) + '. ' + str(card.name) + ' ' + str(card.suit) + \
                     ' ' + str(card.value)
            i += 1
            text += '\n' + output
        return text


@bot.callback_query_handler(func=lambda call: True, state=Blackjack.start)
def start_blackjack(call):
    try:
        player = Player(Deck())
        player.hand_print()
        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            data['player'] = player
        if player.sum == 21:
            bot.send_message(call.from_user.id, player.hand_print())
            gaming_blackjack(call)
        elif player.sum > 21:
            bot.send_message(call.from_user.id, player.hand_print())
            gaming_blackjack(call)
        else:
            bot.send_message(call.from_user.id, player.hand_print() + '\nЕщё?',
                             reply_markup=bj_ore_or_stop())
        bot.set_state(call.from_user.id, Blackjack.gaming,
                      call.message.chat.id)

    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=Blackjack.gaming)
def gaming_blackjack(call):
    try:
        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            player = data['player']
        if call.data == 'm':
            player.take_card()
            bot.set_state(call.from_user.id, Blackjack.gaming,
                          call.message.chat.id)
            bot.send_message(call.from_user.id, player.computer_hand_print())
            bot.send_message(call.from_user.id, player.hand_print(),
                             reply_markup=bj_ore_or_stop())
        else:
            bot.send_message(call.from_user.id, player.computer_hand_print())

            text = 'Игра закончена\n'
            if player.sum == 21:
                text += 'Вы выиграли!'
            elif player.sum > 21:
                text += 'Вы проиграли!'
            elif player.sum == player.computer_sum:
                text += 'Ничья.'
            elif player.sum > player.computer_sum:
                text += 'Вы выиграли!'

            else:
                text += 'Вы проиграли!'

            text += '\nСыграем еще?!'
            bot.send_message(call.from_user.id, text,
                             reply_markup=bj_yes_or_no())
            bot.set_state(call.from_user.id, Blackjack.finish,
                          call.message.chat.id)

    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=Blackjack.finish)
def finish_blackjack(call):
    try:
        bot.reset_data(call.from_user.id)

        if call.data == 'n':
            bot.set_state(call.from_user.id, None, call.message.chat.id)

        else:
            try:
                player = Player(Deck())
                player.hand_print()
                with bot.retrieve_data(call.from_user.id,
                                       call.message.chat.id) as data:
                    data['player'] = player
                if player.sum == 21:
                    bot.send_message(call.from_user.id, player.hand_print())
                    gaming_blackjack(call)
                elif player.sum > 21:
                    bot.send_message(call.from_user.id, player.hand_print())
                    gaming_blackjack(call)
                else:
                    bot.send_message(call.from_user.id, player.hand_print() +
                                     '\nЕщё?', reply_markup=bj_ore_or_stop())
                bot.set_state(call.from_user.id, Blackjack.gaming,
                              call.message.chat.id)

            except Exception as e:
                hotels_log.logger.exception(e)
    except Exception as e:
        hotels_log.logger.exception(e)
