#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A Bot to integrate WhatsApp with Telegram

import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

PHONE_NUMBER, CONFIRMATION_CODE = range(2)


def start(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Hi! I\'m a WhatsGram bot. I can forward your messages to WhatsApp and send your WhatsApp'
                         'messages here.\n\n'
                         'First, what\'s your phone number linked to WhatsApp account?')

    return PHONE_NUMBER


def phone_number(bot, update):
    user = update.message.from_user
    logger.info("Phone number of %s: %s" % (user.first_name, update.message.text))
    bot.sendMessage(update.message.chat_id, text='Now please give me a confirmation code, so I can'
                                                 'log into your WhatsApp account.')

    return CONFIRMATION_CODE


def confirmation_code(bot, update):
    user = update.message.from_user
    logger.info("Confirmation code of %s: %s" % (user.first_name, update.message.text))
    bot.sendMessage(update.message.chat_id, text='Thank you! Now you can start using me.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.sendMessage(update.message.chat_id, text='Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


def main():
    # Create the EventHandler and pass it your bot's token.
    with open("token", "r") as token_file:
        token = token_file.readline()

    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states PHONE_NUMBER, CONFIRMATION_CODE
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],

                                       states={PHONE_NUMBER: [MessageHandler([Filters.text], phone_number)],
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


if __name__ == '__main__':
    main()
