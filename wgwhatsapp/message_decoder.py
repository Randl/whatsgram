import datetime
import logging

import wgcore.message as mess

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def decode_raw_whasapp_message(self, message):
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
        result = mess.Message(message.getBody(), message_date, message.getId(), sender, group)
    elif message.getType() == 'media':
        if message.getMediaType() in ('image', 'audio', 'video'):
            result = mess.mediamessag(message.getBody(), message_date, message.getId(), sender, group,
                                      message.getMediaType(), message.getMediaSize(), message.getMediaUrl())
        elif message.getMediaType() == 'vcard':
            result = mess.VCardMessage(message.getBody(), message_date, message.getId(), sender, group,
                                       message.getCardData())
        elif message.getMediaType() == 'location':
            result = mess.LocationMessage(message.getBody(), message_date, message.getId(), sender, group,
                                          message.getLongitude(), message.getLatitude())
        else:
            result = mess.Message('Unknown media type: {}'.format(message.getMediaType()), message_date,
                                  message.getId(), sender, group)
            logger.error('Unknown media type {} for message {} '.format(message.getMediaType(), message))
    else:
        result = mess.Message('Unknown message type: {}'.format(message.getType()), message_date, message.getId(),
                              sender, group)
        logger.error('Unknown message type {} for message {} '.format(message.getType(), message))

    return result
