import datetime
import logging

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Message:
    def __init__(self, text='', date=datetime.datetime.now(), id='', sender='', conversation=''):
        self.text = text
        self.date = date
        self.id = id
        self.sender = sender
        self.conversation = conversation  # TODO: conversation

    def __str__(self):
        return 'Message {} send on {} from {} in coversation {}:\n{}'.format(self.id, self.date, self.sender,
                                                                             self.conversation, self.text)

    def __repr__(self):
        return str((self.id, self.date, self.sender, self.conversation, self.text))
