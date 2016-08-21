import logging

from telegram import (ReplyKeyboardMarkup, ParseMode)  # pip install python-telegram-bot
from telegram.ext import (CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler)

from wgcore.phonenumber_parse import get_cc_and_number
from wgwhatsapp.wa_registration import requestCodeWA, registerWA

# temporary workaround for localization
_ = lambda x: x

PHONE_NUMBER, PREFIX_CONFIRM, PREFIX_MANUAL, CONFIRMATION_CODE = range(4)

logger = logging.getLogger(__name__)


def createHandler():
    conv_handler = ConversationHandler(entry_points=[CommandHandler('register', register)],

                                       states={PHONE_NUMBER: [MessageHandler([Filters.text], phone_number)],
                                               PREFIX_CONFIRM: [RegexHandler('^(Yes|No)$', prefix_confirm)],
                                               PREFIX_MANUAL: [MessageHandler([Filters.text], prefix_manual)],
                                               CONFIRMATION_CODE: [MessageHandler([Filters.text], confirmation_code)]},

                                       fallbacks=[CommandHandler('cancel', cancel)])
    return conv_handler


####################
# Callback Methods #
####################

def cancel(bot, update):
    user = update.message.from_user
    logger.info('User {} canceled the conversation.'.format(user.id))
    bot.sendMessage(update.message.chat_id, text='Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def register(bot, update):
    user = update.message.from_user
    logger.info(
        'User {}({} aka {} {}) starts conversation.'.format(user.id, user.username, user.first_name, user.last_name))
    bot.sendMessage(update.message.chat_id,
                    text='Hi! I\'m a WhatsGram bot. I can forward your messages to WhatsApp and send your WhatsApp '
                         'messages here.\n\n'
                         'First, what\'s your phone number linked to WhatsApp account? Enter it in international'
                         ' format, starting with \'+\' and international code.')

    return PHONE_NUMBER


country_code = ''
phonenum = ''


def phone_number(bot, update):
    user = update.message.from_user
    global phonenum  # TODO: db
    phonenum = update.message.text
    logger.info('Phone number of user {}: {}'.format(user.id, update.message.text))
    global country_code
    [country_code, phonenum] = get_cc_and_number(phonenum)
    if country_code == '':
        bot.sendMessage(update.message.chat_id, text='Sorry, you entered invalid number. Please, try again.')
        return PHONE_NUMBER

    reply_keyboard = [['Yes', 'No']]

    bot.sendMessage(update.message.chat_id, text='Is *{}* your country code?'.format(country_code),
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                    parse_mode=ParseMode.MARKDOWN)
    return PREFIX_CONFIRM


def prefix_confirm(bot, update):
    user = update.message.from_user
    if update.message.text == 'Yes':
        logger.info('Prefix of user {} confirmed: {}'.format(user.id, country_code))

        bot.sendMessage(update.message.chat_id, text='Now please give me a confirmation code, so I can '
                                                     'log into your WhatsApp account. If you haven\'t got one '
                                                     'please type /retry . You can try voice activation '
                                                     'instead of sms as well by typing /voice')  # TODO: retry, voice
        requestCodeWA(country_code, phonenum)
        return CONFIRMATION_CODE
    else:
        logger.warning('Country code of user {} is wrong. Number: {}'.format(user.id, country_code, phonenum))
        bot.sendMessage(update.message.chat_id, text='What is your country code?')
        return PREFIX_MANUAL


def prefix_manual(bot, update):
    user = update.message.from_user
    global country_code
    country_code = update.message.text
    logger.info('Prefix of user {} is {}'.format(user.id, country_code))

    requestCodeWA(country_code, phonenum)  # TODO: error handling
    bot.sendMessage(update.message.chat_id, text='Now please give me a confirmation code, so I can '
                                                 'log into your WhatsApp account.')
    return CONFIRMATION_CODE


def confirmation_code(bot, update):
    user = update.message.from_user
    code = update.message.text
    logger.info('Confirmation code of user {}: {}'.format(user.id, code))
    code = code.replace('-', '')
    if len(code) == 6 and code.isdigit():
        registerWA(country_code, phonenum, code)
        bot.sendMessage(update.message.chat_id, text='Thank you! Now you can start using me.')

        return ConversationHandler.END
    else:
        bot.sendMessage(update.message.chat_id, text='Sorry, the code you entered is invalid.\n'
                                                     'Confirmation code consists of 6 digits. Please, try again:')
        return CONFIRMATION_CODE
