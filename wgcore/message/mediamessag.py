import datetime
import logging

from wgcore.message import Message

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class MediaMessage(Message):
    def __init__(self, text='', date=datetime.datetime.now(), id='', sender='', conversation='', media_type='',
                 media_size=0, media_url=''):
        super(MediaMessage, self).__init__(text, date, id, sender, conversation)
        self.media_type = media_type
        self.media_size = media_size
        self.media_url = media_url
