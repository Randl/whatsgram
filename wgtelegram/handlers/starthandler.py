from telegram.ext import CommandHandler
import telegram

def createHandler():
    return CommandHandler('start', callback)


####################
# Callback Methods #
####################

def callback(bot, update):
    bot.sendMessage(update.message.chat_id, "Please run /register to register");