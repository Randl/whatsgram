import datetime
import logging

from wgcore.message.message import Message

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class LocationMessage(Message):
    def __init__(self, text='', date=datetime.datetime.now(), id='', sender='', conversation='', latitude=0.0,
                 longitude=0.0):
        super(LocationMessage, self).__init__(text, date, id, sender, conversation)
        self.longitude = longitude
        self.latitude = latitude
    
    def __str__(self):
        return 'Location message {} send on {} from {} in coversation {}:\nLatitude: {}\nLongitude: {}'.format(self.id,
                                                                                                               self.date,
                                                                                                               self.sender,
                                                                                                               self.conversation,
                                                                                                               self.text,
                                                                                                               self.latitude,
                                                                                                               self.longitude)
    
    def __repr__(self):
        return str((self.id, self.date, self.sender, self.conversation, self.text, self.latitude, self.longitude))
