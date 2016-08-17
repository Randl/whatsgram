import logging
import threading

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class EchoLayer(YowInterfaceLayer):
    def __init__(self):
        super(EchoLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()
        self.message_list = []

    @ProtocolEntityCallback('message')
    def onMessage(self, message):
        """
        When new message arrives, adds it to message list and sends receipt.
        :param message: new message
        :return: void
        """

        self.message_list.append(message)

        # send receipt
        self.toLower(message.ack(False))

        logger.info('Message received')

    @ProtocolEntityCallback('receipt')
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), 'receipt', entity.getType(), entity.getFrom())
        self.toLower(ack)

    def send_message(self, phone, message):
        """
        Sends message
        :param phone: Recipient of the message (phone or phone-group)
        :param message: Message to send
        :return: void
        """
        self.lock.acquire()
        if '@' in phone:  # full adress
            entity = TextMessageProtocolEntity(message, to=phone)
        elif '-' in phone:  # group
            entity = TextMessageProtocolEntity(message, to='{}@g.us'.format(phone))
        else:  # number only
            entity = TextMessageProtocolEntity(message, to='{}@s.whatsapp.net'.format(phone))

        self.ackQueue.append(entity.getId())
        self.toLower(entity)
        self.lock.release()

    @ProtocolEntityCallback('ack')
    def onAck(self, entity):
        self.lock.acquire()

        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            logger.info('Message sent')

        self.lock.release()
