import datetime
import logging
import threading
from time import sleep

from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.stacks import YowStackBuilder  # pip install yowsup2

from whatsapp_layer import EchoLayer

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def decode_message(message):
    """
    Decodes message
    :param message: raw message
    :return: Dictionary with four fields: date, id, from and message
    """
    if message.getType() == 'text':
        # self.output(message.getBody(), tag = '%s [%s]'%(message.getFrom(), formattedDate))
        message_body = message.getBody()
    elif message.getType() == 'media':
        if message.getMediaType() in ("image", "audio", "video"):
            message_body = {'type': message.getMediaType(), 'size': message.getMediaSize(),
                            'url': message.getMediaUrl()}
        elif message.getMediaType() == 'vcard':
            message_body = {'name': message.getName(), 'vcard': message.getCardData()}
        elif message.getMediaType() == 'location':
            message_body = {'latitude': message.getLatitude(), 'longitude': message.getLongitude()}
        else:
            message_body = 'Unknown media type: {}'.format(message.getMediaType())
            logger.error('Unknown media type {} for message {} '.format(message.getMediaType(), message))
    else:
        message_body = 'Unknown message type {} '.format(message.getType())
        logger.error('Unknown message type {} for message {} '.format(message.getType(), message))

    formattedDate = datetime.datetime.fromtimestamp(message.getTimestamp()).strftime('%d-%m-%Y %H:%M:%S')
    sender = message.getFrom() if not message.isGroupMessage() else "{}/{}".format(message.getParticipant(False),
                                                                                   message.getFrom())
    output = {'date': formattedDate, 'id': message.getId(), 'from': sender, 'message': message_body}
    return output


class WhatsApp:
    def __init__(self, read=False):
        # TODO: user/.yowsup/phonenumber/axolotl.db must be removed if someone changed device, else untrusted identity
        self.read_notify = read

        self.echoLayer = EchoLayer()
        stackBuilder = YowStackBuilder()
        self.stack = stackBuilder.pushDefaultLayers(True).push(self.echoLayer).build()

        config = {}
        with open("config", "r") as config_file:
            for line in config_file:
                (key, val) = line.split(' ')
                config[key] = val.strip()
        # credentials
        self.credentials = (config['whatsupnum'], config['whatsuppass'].encode())

        self.stack.setCredentials(self.credentials)

        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))  # sending the connect signal

        self.thread = threading.Thread(target=self.stack.loop)
        self.thread.start()

    def stop(self):
        logger.info("Stoping loop")  # TODO:
        self.thread.join()

    def send_message(self, destination, message):
        """
        destination is <phone number> without '+' and with country code of type string, message is string e.g
        send_message('11133434343','hello')
        """
        self.echoLayer.send_message(destination, message)
        logger.info("Exiting message sending function")

    def get_messages(self):
        """
        Returns and clears list of all received messages, marks messages as read if chosen.
        """
        tmp = self.echoLayer.message_list.copy()
        if self.read_notify:
            for mess in tmp:
                self.echoLayer.toLower(mess.ack(True))
        self.echoLayer.message_list.clear()
        logger.info("Exiting message receiving function")
        return tmp


if __name__ == '__main__':
    w = WhatsApp(True)
    while True:
        x = w.get_messages()
        if len(x) != 0:
            for m in x:
                print("{}".format(decode_message(m)))
            print("no new messages")
        sleep(10)
