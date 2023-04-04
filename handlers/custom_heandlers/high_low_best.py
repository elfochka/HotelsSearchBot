from database.bd_history import add_entry
from keyboards.inline.keyboard import inline_yes_or_no, inline_numbers
from loader import bot
from hotlog import hotels_log
from states.request_data import HighLowBest
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from api import general
from telebot.types import InputMediaPhoto
import datetime
from datetime import datetime as dt


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_command(message) -> None:
    """
    ловим команды 'lowprice', 'highprice', 'bestdeal'
    Запрашиваем город у пользователя и записываем команду
    :param message: сообщение пользователя
    :return: (None)
    """
    bot.set_state(message.from_user.id, HighLowBest.command, message.chat.id)
    text = 'Введите город для поиска отелей.'
    bot.send_message(message.from_user.id, text)
    bot.set_state(message.from_user.id, HighLowBest.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id
        data['command'] = message.text
        data['history'] = False


@bot.message_handler(state=HighLowBest.city)
def get_city(message) -> None:
    """
    Запрашиваем дату заезда у пользователя и записываем город
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        text = 'Спасибо, записал. Теперь введите дату заезда'
        bot.send_message(message.from_user.id, text)
        calendar, step = \
            DetailedTelegramCalendar(locale='ru',
                                     min_date=datetime.date.today()).build()
        bot.send_message(message.chat.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)
        bot.set_state(message.from_user.id, HighLowBest.check_in,
                      message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(),
                            state=HighLowBest.check_in)
def callback_check_in(message) -> None:
    """
    Запрашиваем дату отъезда у пользователя и записываем дату заезда
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        result, key, step = \
            DetailedTelegramCalendar(
                locale='ru', min_date=datetime.date.today()
            ).process(message.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  message.message.chat.id,
                                  message.message.message_id,
                                  reply_markup=key)
        elif result:
            text = 'Спасибо, записал. Теперь введите дату отъезда'
            bot.send_message(message.from_user.id, text)

            check_in = str(result)

            with bot.retrieve_data(message.from_user.id,
                                   message.message.chat.id) as data:
                data['check_in'] = check_in
                min_date = dt.strptime(check_in, "%Y-%m-%d").date()

            calendar, step = DetailedTelegramCalendar(
                locale='ru', min_date=min_date
            ).build()
            bot.send_message(message.message.chat.id,
                             f"Select {LSTEP[step]}",
                             reply_markup=calendar)

            bot.set_state(message.from_user.id,
                          HighLowBest.check_out, message.message.chat.id)
    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(),
                            state=HighLowBest.check_out)
def callback_check_out(message) -> None:
    """
    Запрашиваем количество отелей для вывода у пользователя
    и записываем дату отъезда
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        with bot.retrieve_data(message.from_user.id, message.message.chat.id) \
                as data:
            min_date = data['check_in']
        check_in = dt.strptime(str(min_date), "%Y-%m-%d").date()
        result, key, step = DetailedTelegramCalendar(
            locale='ru', min_date=check_in).process(message.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  message.message.chat.id,
                                  message.message.message_id,
                                  reply_markup=key)
        elif result:
            text = 'Спасибо, записал. Теперь введите количество отелей, ' \
                   'которые необходимо вывести в результате (не больше 10)'
            bot.send_message(message.from_user.id, text,
                             reply_markup=inline_numbers(10))
            bot.set_state(message.from_user.id, HighLowBest.number_hotels,
                          message.message.chat.id)

            check_out = str(result)

            with bot.retrieve_data(message.from_user.id,
                                   message.message.chat.id) as data:
                data['check_out'] = check_out
    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=HighLowBest.number_hotels)
def get_number_hotels(call) -> None:
    """
    Запрашиваем нужны ли фотографии отеля у пользователя
     и записываем количество отелей
    :param call: отклик пользователя
    :return: (None)
    """
    try:
        if call.data and 0 < int(call.data) <= 10:
            bot.send_message(call.from_user.id,
                             'Спасибо, записал. '
                             'Необходимо ли выводить фотографии '
                             'для каждого отеля?',
                             reply_markup=inline_yes_or_no())
            bot.set_state(call.from_user.id, HighLowBest.need_photo_yes_or_no,
                          call.message.chat.id)

            with bot.retrieve_data(call.from_user.id,
                                   call.message.chat.id) as data:
                data['number_hotels'] = int(call.data)
        else:
            bot.send_message(call.from_user.id, 'Вам необходимо '
                                                'ввести число от 1 до 10')
    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=HighLowBest.need_photo_yes_or_no)
def get_need_photo_yes_or_no(call) -> None:
    """
    Запрашиваем количество фотографий каждого отеля у пользователя
    и записываем нужны ли фотографии отеля
    :param call: отклик пользователя
    :return: (None)
    """
    try:
        if call.data == 'Да':

            bot.send_message(call.from_user.id,
                             'Введите количество фотографий '
                             'для каждого отеля (не больше 5ти)',
                             reply_markup=inline_numbers(5))
            bot.set_state(call.from_user.id, HighLowBest.number_photos,
                          call.message.chat.id)

        elif call.data == 'Нет':

            with bot.retrieve_data(call.from_user.id,
                                   call.message.chat.id) as data:

                data['number_photos'] = 0

                number_photos = data['number_photos']
                text = f'Ищу отели для Вас в городе *{data["city"]}* ' \
                       f'с *{data["check_in"]}* по *{data["check_out"]}*, ' \
                       f'количество отелей *{data["number_hotels"]}*, ' \
                       f'количество фотографий *{data["number_photos"]}*. ' \
                       f'Это может занять 1-5 минут...'

                bot.send_message(call.from_user.id,
                                 text, parse_mode="Markdown")

                general_response = general.general(data)
            send_result(call, general_response, number_photos)

        else:
            bot.send_message(call.from_user.id, 'Нужно нажать на кнопку '
                                                '"Да" или "Нет"')
    except Exception as e:
        hotels_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=HighLowBest.number_photos)
def get_number_photos(call) -> None:
    """
    Обработка запроса к API
    :param call: отклик пользователя
    :return: (None)
    """
    try:
        if bot.get_state(call.from_user.id, call.message.chat.id) is None:
            bot.set_state(call.from_user.id, HighLowBest.number_photos,
                          call.message.chat.id)

        if call.data.isdigit() and 0 < int(call.data) <= 5:
            with bot.retrieve_data(call.from_user.id,
                                   call.message.chat.id) as data:
                data['number_photos'] = int(call.data)
                number_photos = data['number_photos']
                text = f'Ищу отели для Вас в городе *{data["city"]}* ' \
                       f'с *{data["check_in"]}* по *{data["check_out"]}*, ' \
                       f'количество отелей *{data["number_hotels"]}*, ' \
                       f'количество фотографий *{data["number_photos"]}*. ' \
                       f'Это может занять 1-5 минут...'

                bot.send_message(call.from_user.id, text,
                                 parse_mode="Markdown")
                general_response = general.general(data)

            send_result(call, general_response, number_photos)
        else:
            bot.send_message(call.from_user.id, 'Вам необходимо '
                                                'ввести число от 1 до 5')
    except Exception as e:
        hotels_log.logger.exception(e)


def send_result(call, general_response, number_photos) -> None:
    """
    Вывод результата пользователю
    :param call: отклик пользователя
    :param general_response: вывод API
    :param number_photos: кол-во фото
    :return: (None)
    """
    try:
        bot.set_state(call.from_user.id, HighLowBest.result,
                      call.message.chat.id)

        if general_response:
            with bot.retrieve_data(call.from_user.id,
                                   call.message.chat.id) as data:
                check_in = data['check_in']
                check_out = data['check_out']

            i = 1
            for hotel in general_response:
                text = f'{i}. *{hotel["name"]}*\n' \
                       f'Рейтинг: {hotel["rating"]} из 10\n' \
                       f'Даты путешествия: с {check_in} по {check_out}\n' \
                       f'Стоимость за ночь: {hotel["price"]}\n' \
                       f'Полная стоимость: {hotel["total_price"]}\n' \
                       f'Адрес: {hotel["address"]}\n' \
                       f'[Перейти на сайт для бронирования](' \
                       f'hoteles.com/ho351815/?chkin={check_in}' \
                       f'&chkout={check_out}&x_pwa=1&rfrr=HSR&' \
                       f'pwa_ts=1680482008097&referrerUrl=' \
                       f'aHR0cHM6Ly9hci5ob3RlbGVzLmNvbS9Ib3RlbC1TZWFyY2g' \
                       f'%3D&useRewards=false&rm1=a2&regionId=8281&' \
                       f'selected={hotel["hotel_id"]}&sort=RECOMMENDED&' \
                       f'top_dp=37883&top_cur=ARS&userIntent=&' \
                       f'selectedRoomType=314426472&selectedRatePlan=' \
                       f'383482768&expediaPropertyId={hotel["hotel_id"]}' \
                       f')'

                if number_photos > 0:
                    media = [InputMediaPhoto(hotel["preview_photo"],
                                             caption=text,
                                             parse_mode="Markdown")]
                    for photo in hotel["photos"]:
                        media.append(InputMediaPhoto(photo))

                    bot.send_media_group(call.message.chat.id, media)
                else:
                    bot.send_message(call.from_user.id, text,
                                     parse_mode="Markdown")

                i += 1
            do_finish(call)

        else:
            bot.send_message(call.from_user.id, 'Отелей по Вашему '
                                                'запросу не найдено!')
            do_finish(call)

    except Exception as e:
        hotels_log.logger.exception(e)


def do_finish(call) -> None:
    """
    Сохраняем запрос в базу данных и стираем data и обнуляем State
    :param call: отклик пользователя
    :return: (None)
    """
    try:
        bot.set_state(call.from_user.id, HighLowBest.finish,
                      call.message.chat.id)

        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            if not data['history']:
                data = dict(data)

                add_entry(data)
        try:
            bot.reset_data(call.from_user.id)
            bot.set_state(call.from_user.id, None, call.message.chat.id)
        except Exception as e:
            hotels_log.logger.exception(e)

    except Exception as e:
        hotels_log.logger.exception(e)
