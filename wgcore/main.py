import logging
import wgtelegram.tgbot as tg

logger = logging.getLogger(__name__)

def runWhatsgram():
    config = {}
    with open('config', 'r') as config_file:
        for line in config_file:
            (key, val) = line.split(' ')
            config[key] = val.strip()
    startTelegram(config)
    

def startTelegram(config):
    telegram = tg.TGBot(config['token'])
    telegram.registerHandlers()
    telegram.start()
    #TODO: make it stop able via command
    telegram.idle()