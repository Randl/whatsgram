import logging

from telegram.ext import (Updater)

from wgtelegram.handlers import (registerhandler, starthandler)

logger = logging.getLogger(__name__)


class TGBot:
    def __init__(self, token):
        # Create the EventHandler and pass it your bot's token.
        logger.info('Connecting...')
        try:
            self.updater = Updater(token)
            self.dispatcher = self.updater.dispatcher
            logger.info('Connected as ' + self.updater.bot.getMe().username)
        except:
            logger.error('Could not connect and get self! (Wrong bot token?)!')

    def registerHandlers(self):
        def error(bot, update, err):
            logger.warn('Update \'{}\' caused error \'{}\''.format(update, err))

        try:
            logger.info('Registering handlers...')

            # register all handlers (TODO: make dynamic)
            self.dispatcher.add_handler(starthandler.createHandler())
            self.dispatcher.add_handler(registerhandler.createHandler())

            # log all errors
            self.dispatcher.add_error_handler(error)
            logger.info('Registered 2 handlers')

        except:
            logger.error('Could not register handlers!')

    def start(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def idle(self):
        self.updater.idle()
