import datetime
import logging

from wgcore.message.locationmessage import LocationMessage
from wgcore.message.mediamessage import MediaMessage
from wgcore.message.message import Message
from wgcore.message.vcardmessage import VCardMessage

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def decode_raw_whasapp_message(message):
    """
    Decodes message
    :param message: raw message
    :return: Message object
    """

    message_date = datetime.datetime.fromtimestamp(message.getTimestamp())  # .strftime('%d-%m-%Y %H:%M:%S')
    sender = message.getFrom() if not message.isGroupMessage() else message.getParticipant(False)
    group = '' if not message.isGroupMessage() else message.getFrom()  # TODO get conversation number from database
    # instead
    if message.getType() == 'text':
        # self.output(message.getBody(), tag = '%s [%s]'%(message.getFrom(), formattedDate))
        result = Message(message.getBody(), message_date, message.getId(), sender, group)
    elif message.getType() == 'media':
        if message.getMediaType() in ('image', 'audio', 'video'):
            result = MediaMessage(message.getBody(), message_date, message.getId(), sender, group,
                                  message.getMediaType(), message.getMediaSize(), message.getMediaUrl())
        elif message.getMediaType() == 'vcard':
            result = VCardMessage(message.getBody(), message_date, message.getId(), sender, group,
                                  message.getCardData())
        elif message.getMediaType() == 'location':
            result = LocationMessage(message.getBody(), message_date, message.getId(), sender, group,
                                     message.getLongitude(), message.getLatitude())
        else:
            result = Message('Unknown media type: {}'.format(message.getMediaType()), message_date,
                             message.getId(), sender, group)
            logger.error('Unknown media type {} for message {} '.format(message.getMediaType(), message))
    else:
        result = Message('Unknown message type: {}'.format(message.getType()), message_date, message.getId(), sender,
                         group)
        logger.error('Unknown message type {} for message {} '.format(message.getType(), message))

    return result
