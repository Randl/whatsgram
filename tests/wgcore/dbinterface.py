import logging

from wgcore.dbinterface import DBInterface
from wgcore.message.locationmessage import LocationMessage
from wgcore.message.message import Message

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

db = DBInterface()
db.clear()
db.add_user('12', '79101234567')
conv = db.add_conversation('12', '796110234532')
mess = LocationMessage(text='hi!', id='0', sender='796110234532', conversation=conv, longitude=72.36, latitude=22.18)
mess2 = Message(text='hi!hi', id='2', sender='796110234532', conversation=conv)
db.add_message(conv, mess)
db.add_message(conv, mess2)
print(db.get_conversations('12'))
print(db.get_messages(conv))
db.clear()
