import logging

from wgcore.phonenumber_parse import get_cc_and_number
from wgwhatsapp.wa_registration import register, requestCode
from wgwhatsapp.wabot import WABot

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

config = {}
with open('config', 'r') as config_file:
    for line in config_file:
        (key, val) = line.split(' ')
        config[key] = val.strip()


def test_reg():
    country_code = get_cc_and_number('+' + config['whatsupnum'])
    requestCode(country_code[0], country_code[1])
    code = input('Please enter the code: ')
    config['whatsuppass'] = register(config['whatsupnum'], country_code[0], country_code[1])


def test_bot():
    bot = WABot(config['whatsupnum'], config['whatsuppass'], True)
