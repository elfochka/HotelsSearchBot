from keyboards.reply.yes_or_no import request_yes_or_no
from loader import bot
import requests
from telebot.types import Message
from states.request_data import UserSearchParam


# import highprice


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message) -> None:
    # bot.delete_state(message.from_user.id, message.chat.id)
    # low_data = {}

    bot.send_message(message.from_user.id, 'Введите город для поиска отелей.')
    bot.set_state(message.from_user.id, UserSearchParam.city, message.chat.id)


# @bot.message_handler(commands=['highprice'])
# def bot_highprice(message: Message) -> None:
#     # bot.delete_state(message.from_user.id, message.chat.id)
#     # high_data = {}
#
#     bot.send_message(message.from_user.id, 'Введите город для поиска отелей.')
#     bot.set_state(message.from_user.id, UserSearchParam.city, message.chat.id)


@bot.message_handler(state=UserSearchParam.city)
def get_city(message: Message) -> None:
    text = 'Спасибо, записал. Теперь введите количество отелей, которые необходимо вывести в результате (не больше 10)'
    bot.send_message(message.from_user.id, text)
    bot.set_state(message.from_user.id, UserSearchParam.number_hotels, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as low_data:
        low_data['city'] = message.text


@bot.message_handler(state=UserSearchParam.number_hotels)
def get_number_hotels(message: Message) -> None:
    if message.text.isdigit() and 0 < int(message.text) <= 10:
        bot.send_message(message.from_user.id,
                         'Спасибо, записал. Необходимо ли выводить фотографии для каждого отеля?',
                         reply_markup=request_yes_or_no())
        bot.set_state(message.from_user.id, UserSearchParam.need_photo_yes_or_no, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as low_data:
            low_data['number_hotels'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Вам необходимо ввести число от 1 до 10')


@bot.message_handler(content_types=['text'], state=UserSearchParam.need_photo_yes_or_no)
def get_need_photo_yes_or_no(message: Message) -> None:
    # print(message.text)
    if message.text == 'Да':
        bot.send_message(message.from_user.id,
                         'Введите количество фотографий для каждого отеля (не больше 5ти)')
        bot.set_state(message.from_user.id, UserSearchParam.number_photos, message.chat.id)

    elif message.text == 'Нет':

        with bot.retrieve_data(message.from_user.id, message.chat.id) as low_data:

            low_data['number_photos'] = 0

            text = f'Ищу отели по заданным параметрам:\n' \
                   f'Город - {low_data["city"]} \n' \
                   f'Количество отелей в поиске - {low_data["number_hotels"]}\n' \
                   f'Без фотографий'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Нужно нажать на кнопку "Да" или "Нет"')


@bot.message_handler(state=UserSearchParam.number_photos)
def get_number_hotels(message: Message) -> None:
    if message.text.isdigit() and 0 < int(message.text) <= 5:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as low_data:

            low_data['number_photos'] = int(message.text)

            text = f'Ищу отели по заданным параметрам:\n' \
                   f'Город - {low_data["city"]} \n' \
                   f'Количество отелей в поиске - {low_data["number_hotels"]}\n' \
                   f'Фотографий каждого отеля - {low_data["number_photos"]}'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Вам необходимо ввести число от 1 до 10')
    print(low_data)






    # url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    #
    # querystring = {"q": "new york", "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    #
    # headers = {
    #     "X-RapidAPI-Key": config.RAPID_API_KEY,
    #     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    # }
    #
    # response = requests.request("GET", url, headers=headers, params=querystring)
    #
    # print(response.text)
