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

    @ProtocolEntityCallback("message")
    def onMessage(self, message):
        if message.getType() == 'text':
            self.message_list.append((message.getFrom(), message.getBody()))
        # send receipt otherwise we keep receiving the same message over and over
        # receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
        # self.toLower(receipt)
        self.toLower(message.ack(True))
        logger.info("Message received")

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)

    def send_message(self, phone, message):
        self.lock.acquire()
        if '@' in phone:
            entity = TextMessageProtocolEntity(message, to=phone)
        elif '-' in phone:
            entity = TextMessageProtocolEntity(message, to="%s@g.us" % phone)
        else:
            entity = TextMessageProtocolEntity(message, to="%s@s.whatsapp.net" % phone)
        self.ackQueue.append(entity.getId())
        self.toLower(entity)
        logger.info("Message sent")
        self.lock.release()

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()

        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            logger.info("Message sent")

        self.lock.release()
