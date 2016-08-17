import logging
import threading

from yowsup.layers import YowLayerEvent  # pip install yowsup2
from yowsup.layers.network import YowNetworkLayer
from yowsup.stacks import YowStackBuilder

from wgwhatsapp.layers.echolayer import EchoLayer

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class WABot:
    def __init__(self, read=False):
        # TODO: user/.yowsup/phonenumber/axolotl.db must be removed if someone changed device, else untrusted identity
        self.read_notify = read

        self.echoLayer = EchoLayer()
        stackBuilder = YowStackBuilder()
        self.stack = stackBuilder.pushDefaultLayers(True).push(self.echoLayer).build()

        config = {}
        with open('config', 'r') as config_file:
            for line in config_file:
                (key, val) = line.split(' ')
                config[key] = val.strip()
        # credentials
        self.credentials = (config['whatsupnum'], config['whatsuppass'].encode())
        logger.info('Connecting as {}'.format(config['whatsupnum']))

        self.stack.setCredentials(self.credentials)

        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))  # sending the connect signal

        self.thread = threading.Thread(target=self.stack.loop)  # message receiver thread

    def start(self):
        logger.info('Starting message receiver thread')
        self.thread.start()

    def stop(self):
        logger.info('Stoping loop')  # TODO:
        self.thread.join()

    def send_message(self, destination, message):
        """
        Send a text message to destiination
        :param destination:  destination is <phone number> without '+' and with country code of type string
        :param message: text string
        :return:
        """
        self.echoLayer.send_message(destination, message)  # TODO: add media
        logger.info('Message to {} sent'.format(destination))

    def get_messages(self):
        """
        Returns and clears list of all received messages, marks messages as read if chosen.
        """
        tmp = self.echoLayer.message_list.copy()
        if self.read_notify:
            for mess in tmp:
                self.echoLayer.toLower(mess.ack(True))
        self.echoLayer.message_list.clear()
        logger.info('Messages received from message list')
        return tmp
