import logging

from telegram import (ReplyKeyboardMarkup, ParseMode)  # pip install python-telegram-bot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler)

from phonenumber_parse import get_prefix

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

PHONE_NUMBER, PREFIX_CONFIRM, PREFIX_MANUAL, CONFIRMATION_CODE = range(4)


def start(bot, update):
    user = update.message.from_user
    logger.info(
        'User {}({} aka {} {}) starts conversation.'.format(user.id, user.username, user.first_name, user.last_name))
    bot.sendMessage(update.message.chat_id,
                    text='Hi! I\'m a WhatsGram bot. I can forward your messages to WhatsApp and send your WhatsApp '
                         'messages here.\n\n'
                         'First, what\'s your phone number linked to WhatsApp account?')

    return PHONE_NUMBER


prefix = ''
def phone_number(bot, update):
    user = update.message.from_user
    phonenum = update.message.text
    logger.info('Phone number of user {}: {}'.format(user.id, update.message.text))
    global prefix
    prefix = get_prefix(phonenum)
    if prefix == '':
        bot.sendMessage(update.message.chat_id, text='Sorry, you entered non-valid number. Please, try again.')
        return PHONE_NUMBER

    reply_keyboard = [['Yes', 'No']]

    bot.sendMessage(update.message.chat_id, text='Is *{}* your country prefix?'.format(prefix),
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                    parse_mode=ParseMode.MARKDOWN)
    return PREFIX_CONFIRM


def prefix_confirm(bot, update):
    user = update.message.from_user
    if (update.message.text == 'Yes'):
        logger.info('Prefix of user {} confirmed: {}'.format(user.id, prefix))
        bot.sendMessage(update.message.chat_id, text='Now please give me a confirmation code, so I can'
                                                 'log into your WhatsApp account.')
        return CONFIRMATION_CODE
    else:
        logger.info('Prefix of user {} is wrong'.format(user.id, prefix))
        bot.sendMessage(update.message.chat_id, text='What is your country prefix?')
        return PREFIX_MANUAL


def prefix_manual(bot, update):
    user = update.message.from_user
    global prefix
    prefix = update.message.text
    logger.info('Prefix of user {} is {}'.format(user.id, prefix))

    bot.sendMessage(update.message.chat_id, text='Now please give me a confirmation code, so I can'
                                                 'log into your WhatsApp account.')
    return CONFIRMATION_CODE

def confirmation_code(bot, update):
    user = update.message.from_user
    logger.info('Confirmation code of user {}: {}'.format(user.id, update.message.text))
    bot.sendMessage(update.message.chat_id, text='Thank you! Now you can start using me.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info('User {} canceled the conversation.'.format(user.id))
    bot.sendMessage(update.message.chat_id, text='Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, err):
    logger.warn('Update \'{}\' caused error \'{}\''.format(update, err))


def bot_print(chat_id, message):
    print('bot print')  # TODO


def run_telegram_bot():
    config = {}
    with open('config', 'r') as config_file:
        for line in config_file:
            (key, val) = line.split(' ')
            config[key] = val.strip()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config['token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states PHONE_NUMBER, CONFIRMATION_CODE
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],

                                       states={PHONE_NUMBER: [MessageHandler([Filters.text], phone_number)],
                                               PREFIX_CONFIRM: [RegexHandler('^(Yes|No)$', prefix_confirm)],
                                               PREFIX_MANUAL: [MessageHandler([Filters.text], prefix_manual)],
                                               CONFIRMATION_CODE: [MessageHandler([Filters.text], confirmation_code)]},

                                       fallbacks=[CommandHandler('cancel', cancel)])

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
