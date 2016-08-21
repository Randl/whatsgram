import logging

from wgcore.phonenumber_parse import get_cc_and_number
from wgwhatsapp.wa_registration import registerWA, requestCodeWA
from wgwhatsapp.wabot import WABot

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

config = {}
with open('config', 'r') as config_file:
    for line in config_file:
        (key, val) = line.split(' ')
        config[key] = val.strip()


def test_reg(method='sms'):
    country_code = get_cc_and_number('+' + config['whatsupnum'])
    logger.info('Code requesting for cc {}, number {}'.format(country_code[0], country_code[1]))
    requestCodeWA(country_code[0], country_code[1], method)
    code = input('Please enter the code: ')
    config['whatsuppass'] = registerWA(country_code[0], country_code[1], code)


def test_bot():
    bot = WABot(config['whatsupnum'], config['whatsuppass'], True)


# test_reg()
test_bot()
