import datetime
import logging

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def decode_message(message):
    """
    Decodes message
    :param message: raw message
    :return: Dictionary with four fields: type, date, id, from and message
    """
    if message.getType() == 'text':
        # self.output(message.getBody(), tag = '%s [%s]'%(message.getFrom(), formattedDate))
        message_body = message.getBody()
        m_type = 'text'
    elif message.getType() == 'media':
        if message.getMediaType() in ('image', 'audio', 'video'):
            message_body = {'type': message.getMediaType(), 'size': message.getMediaSize(),
                            'url': message.getMediaUrl()}
            m_type = 'downloadable_media'
        elif message.getMediaType() == 'vcard':
            message_body = {'name': message.getName(), 'vcard': message.getCardData()}
            m_type = 'vcard'
        elif message.getMediaType() == 'location':
            message_body = {'latitude': message.getLatitude(), 'longitude': message.getLongitude()}
            m_type = 'location'
        else:
            message_body = 'Unknown media type: {}'.format(message.getMediaType())
            logger.error('Unknown media type {} for message {} '.format(message.getMediaType(), message))
    else:
        message_body = 'Unknown message type {} '.format(message.getType())
        logger.error('Unknown message type {} for message {} '.format(message.getType(), message))

    formattedDate = datetime.datetime.fromtimestamp(message.getTimestamp()).strftime('%d-%m-%Y %H:%M:%S')
    sender = message.getFrom() if not message.isGroupMessage() else '{}/{}'.format(message.getParticipant(False),
                                                                                   message.getFrom())
    output = {'date': formattedDate, 'id': message.getId(), 'from': sender, 'message': message_body, 'type': m_type}
    return output
