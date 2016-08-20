import datetime
import logging

from wgcore.message.message import Message

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class LocationMessage(Message):
    def __init__(self, text='', date=datetime.datetime.now(), id='', sender='', conversation='', longitude=0.0,
                 latitude=0.0):
        super(LocationMessage, self).__init__(text, date, id, sender, conversation)
        self.longitude = longitude
        self.latitude = latitude
