from hotlog import hotels_log
from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_commands


try:
    if __name__ == '__main__':
        bot.add_custom_filter(StateFilter(bot))
        set_commands(bot)
        bot.infinity_polling()
except BaseException as e:
    hotels_log.logger.exception(e)
