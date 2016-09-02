import datetime
import logging

from wgcore.message.message import Message

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class VCardMessage(Message):
    def __init__(self, text='', date=datetime.datetime.now(), id='', sender='', conversation='', vcard=''):
        super(VCardMessage, self).__init__(text, date, id, sender, conversation)
        self.vcard = vcard

    def __str__(self):
        return 'vCard Message {} send on {} from {} in coversation {}:\n{}\nvCard data:\n{}'.format(self.id, self.date,
                                                                                                    self.sender,
                                                                                                    self.conversation,
                                                                                                    self.text,
                                                                                                    self.vcard)

    def __repr__(self):
        return str((self.id, self.date, self.sender, self.conversation, self.text, self.vcard))
