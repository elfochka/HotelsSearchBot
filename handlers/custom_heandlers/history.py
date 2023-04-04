from api import general
from database.bd_history import history_output, get_entry
from handlers.custom_heandlers.high_low_best import send_result
from loader import bot
from hotlog import hotels_log
from states.request_data import History
from keyboards.inline.keyboard import hotels_history


@bot.message_handler(commands=['history'])
def bot_history(message) -> None:
    """
    ловим команду history
    :param message: сообщение пользователя
    :return: None
    """
    bot.set_state(message.from_user.id, History.select_search, message.chat.id)
    try:

        history_output_data = history_output(message.from_user.id)
        if history_output_data:

            # history_output_text = []
            #
            # for entry in history_output_data:
            #     history_output_text.append(
            #         f'*{entry[7]}*. Поиск в городе *{entry[2]}*. '
            #         f'С *{entry[3]}* по *{entry[4]}*. '
            #         f'Отелей в выдаче  *{entry[5]}*, с *{entry[6]}* шт.
            #         фото')

            history_output_text = {}

            for entry in history_output_data:
                num_counts = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣',
                              '7️⃣', '8️⃣', '9️⃣', '🔟']
                text_value = f'{num_counts[int(entry[7])-1]} {entry[2]}.\n' \
                             f'{entry[3]}-{entry[4]}. ' \
                             f'(Отелей: {entry[5]}, фото: {entry[6]})'
                history_output_text.update({entry[7]: text_value})

            # history_output_text = '\n'.join(history_output_text)
            bot.set_state(message.from_user.id, History.selection_processing,
                          message.chat.id)
            # print(history_output_text)
            bot.send_message(message.from_user.id, 'История поиска:',
                             reply_markup=hotels_history(history_output_text))

        else:
            bot.send_message(message.from_user.id,
                             'История поиска отсутствует.')

    except Exception as e:
        hotels_log.logger.exception(e)
        bot.send_message(message.from_user.id, 'История поиска отсутствует.')


@bot.callback_query_handler(func=lambda call: True,
                            state=History.selection_processing)
def get_selection_processing(call) -> None:
    """
    Выводим результат по выбранному из истории запросу
    :param call: отклик пользователя
    :return: (None)
    """
    try:
        select_entry = get_entry(call.from_user.id, call.data)
        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            for entry in select_entry:
                data['user_id'] = entry[0]
                data['command'] = entry[1]
                data['city'] = entry[2]
                data['check_in'] = entry[3]
                data['check_out'] = entry[4]
                data['number_hotels'] = int(entry[5])
                data['number_photos'] = int(entry[6])
                data['history'] = True

            number_photos = data['number_photos']
            text = f'Ищу отели для Вас в городе *{data["city"]}* ' \
                   f'с *{data["check_in"]}* по *{data["check_out"]}*, ' \
                   f'количество отелей *{data["number_hotels"]}*, ' \
                   f'количество фотографий *{data["number_photos"]}*. ' \
                   f'Это может занять 1-5 минут...'

            bot.send_message(call.from_user.id, text, parse_mode="Markdown")
            general_response = general.general(data)

        send_result(call, general_response, number_photos)

    except Exception as e:
        hotels_log.logger.exception(e)
