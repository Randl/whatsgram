from telegram.ext import CommandHandler

# temporary workaround for localization
_ = lambda x: x

def createHandler():
    return CommandHandler('start', callback)


####################
# Callback Methods #
####################

def callback(bot, update):
    bot.sendMessage(update.message.chat_id, 'Please run /register to register');
