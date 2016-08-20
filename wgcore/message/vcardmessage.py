import datetime
import logging

from wgcore.message import Message

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class VCardMessage(Message):
    def __init__(self, text='', date=datetime.datetime.now(), id='', sender='', conversation='', vcard=''):
        super(VCardMessage, self).__init__(text, date, id, sender, conversation)
        self.vcard = vcard
