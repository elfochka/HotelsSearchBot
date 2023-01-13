from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
# from utils.set_bot_commands import set_custom_commands

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    # set_custom_commands(bot)
    bot.infinity_polling()

# import telebot
# from dotenv import load_dotenv
# import time
# import os
#
# from lowprice import lowprice
# from highprice import highprice
# from bestdeal import bestdeal
# from history import history
#
# load_dotenv()
# # print('@HotelsSearchBot запущен')
# bot_token = os.getenv('BOT_TOKEN')
# # print(os.getenv('BOT_TOKEN'))
#
# # bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
#
# bot = telebot.TeleBot("5554134140:AAFSbCuuGZ64R9qf389U3BlD74g8x_UiyFQ")
#
#
# @bot.message_handler(content_types=['text'])
# def start(message):
#     help_message = 'Что может бот:\n/lowprice - Узнать топ самых дешёвых отелей в городе\n' \
#                    '/highprice - Узнать топ самых дорогих отелей в городе\n' \
#                    '/bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра ' \
#                    '(самые дешёвые и находятся ближе всего к центру)\n' \
#                    '/history - Узнать историю поиска отелей'
#
#     if message.text == '/hello_world' or 'привет' in message.text.lower():
#         bot.send_message(message.from_user.id, 'Привет я бот для анализа сайта Hotels.com и поиска подходящих отелей')
#
#     elif message.text == '/lowprice':
#         bot.send_message(message.from_user.id, 'Город, где будет проводиться поиск.')
#         # bot.register_next_step_handler(message, lowprice)  # следующий шаг – функция lowprice
#
#     elif message.text == '/highprice':
#         bot.send_message(message.from_user.id, 'Город, где будет проводиться поиск')
#         # bot.register_next_step_handler(message, highprice)  # следующий шаг – функция highprice
#
#     elif message.text == '/bestdeal':
#         bot.send_message(message.from_user.id, 'Город, где будет проводиться поиск')
#         # bot.register_next_step_handler(message, bestdeal)  # следующий шаг – функция bestdeal
#
#     elif message.text == '/history':
#         bot.send_message(message.from_user.id, '...')
#         # bot.register_next_step_handler(message, history)  # следующий шаг – функция history
#
#     else:
#         bot.send_message(message.from_user.id, help_message)


# if __name__ == '__main__':
#
#     while True:
#         try:  # добавляем try для бесперебойной работы
#             bot.polling(none_stop=True)  # запуск бота
#         except:
#             # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'Global except time.sleep(15) - Done')
#             time.sleep(5)  # в случае падения
