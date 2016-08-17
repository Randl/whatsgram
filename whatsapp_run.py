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


class WhatsApp:
    def __init__(self):
        self.echoLayer = EchoLayer()
        stackBuilder = YowStackBuilder()
        self.stack = stackBuilder.pushDefaultLayers(True).push(self.echoLayer).build()

        config = {}
        with open("config", "r") as config_file:
            for line in config_file:
                (key, val) = line.split(' ')
                config[key] = val.strip()
        # credentials.
        self.credentials = (
        config['whatsupnum'], config['whatsuppass'].encode())  # replace with your phone and password

        self.stack.setCredentials(self.credentials)

        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))  # sending the connect signal

        self.thread = threading.Thread(target=self.stack.loop)  # , kwargs={'timeout': 3, 'discrete': 1})
        self.thread.start()

    def stop(self):
        logger.info("Stoping loop")  # TODO:
        self.thread.join()

    def send_message(self, destination, message):
        '''
        destination is <phone number> without '+'
        and with country code of type string,
        message is string
        e.g send_message('11133434343','hello')
        '''
        self.echoLayer.send_message(destination, message)
        logger.info("Exiting message sending function")

    def get_messages(self):
        tmp = self.echoLayer.message_list.copy()
        self.echoLayer.message_list.clear()
        logger.info("Exiting message receiving function")
        return tmp


if __name__ == '__main__':
    w = WhatsApp()
    while True:
        w.send_message('972586486400', 'how r you')
        x = w.get_messages()
        if len(x) != 0:
            for m in x:
                print("{}: {}".format(m[0], m[1]))
        else:
            print("no new messages")
        sleep(10)
