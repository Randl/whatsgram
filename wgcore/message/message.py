import datetime
import logging

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Message:
    def __init__(self, text='', date=datetime.datetime.now(), id='', sender='', group=''):
        self.text = text
        self.date = date
        self.id = id
        self.sender = sender
        self.group = group
