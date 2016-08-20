import datetime
import logging
import sqlite3

try:
    import cPickle as pickle
except:
    import pickle

from wgcore.message.message import Message
from wgcore.message.locationmessage import LocationMessage
from wgcore.message.mediamessage import MediaMessage
from wgcore.message.vcardmessage import VCardMessage

logger = logging.getLogger(__name__)
count = 0
class DBInterface:
    def __init__(self):
        self.db_filename = 'user_data.db'
        self.connection = sqlite3.connect(self.db_filename)
        self.connection.row_factory = sqlite3.Row
        logger.info('Connected to database {}'.format(self.db_filename))
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (user TEXT UNIQUE, whatsapp_id TEXT UNIQUE)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS conversations (id INTEGER NOT NULL UNIQUE, user TEXT, participant TEXT)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS messages (id TEXT UNIQUE, conversation INTEGER NOT NULL, sender TEXT, '
            'timestamp INTEGER NOT NULL, type INTEGER NOT NULL, message_text TEXT, message BLOB)')
        self.connection.commit()

    def add_user(self, user_id, whatsapp_id):
        self.cursor.execute('INSERT INTO users VALUES (:user, :whatsapp)', {'user': user_id, 'whatsapp': whatsapp_id})
        self.connection.commit()
        logger.info('Commiting changes to database {}. User {} added'.format(self.db_filename, user_id))

    def add_conversation(self, user_id, participant):
        # TODO: add ID generator
        global count
        self.cursor.execute('INSERT INTO conversations VALUES (:id, :user, :part)',
                            {'id': count, 'user': user_id, 'part': participant})
        self.connection.commit()
        logger.info('Commiting changes to database {}. Conversation {} added'.format(self.db_filename, count))
        count += 1
        return count -1

    def add_message(self, conversation_id, message):
        if message is MediaMessage:
            type = 'media'
            blob = pickle.dumps((message.media_type, message.media_size, message.media_url), pickle.HIGHEST_PROTOCOL)
        elif message is VCardMessage:
            type = 'vcard'
            blob = pickle.dumps(message.vcard, pickle.HIGHEST_PROTOCOL)
        elif message is LocationMessage:
            type = 'location'
            blob = pickle.dumps((message.longitude, message.latitude), pickle.HIGHEST_PROTOCOL)
        else:
            type = 'text'
            blob = None

        self.cursor.execute(
            'INSERT INTO  messages  VALUES (:id, :conversation, :sender, :timestamp, :type, :txt, :message)',
            {'id': message.id, 'conversation': conversation_id, 'sender': message.sender,
             'timestamp': int(message.date.timestamp()), 'type': type, 'txt': message.text,
             'message': sqlite3.Binary(blob) if blob is not None else None})

        self.connection.commit()
        logger.info('Commiting changes to database {}. Message {} added'.format(self.db_filename, message))

    def get_conversations(self, user_id):  # TODO: create new item on getter if found nothing?
        self.cursor.execute('SELECT id, participant FROM conversations WHERE user = :user', {'user': user_id})
        conv_rows = self.cursor.fetchall()
        convs = []
        for conv in conv_rows:
            convs.append({'id': conv[0], 'participant': conv[1]})
        return convs

    def get_conversation(self, user_id, participant):
        self.cursor.execute('SELECT id, participant FROM conversations WHERE user = :user AND participant = :part',
                            {'user': user_id, 'part': participant})
        conv = self.cursor.fetchone()
        return {'id': conv[0], 'participant': conv[1]}

    def get_messages(self, conversation_id):
        self.cursor.execute('SELECT * FROM messages WHERE conversation = :conv', {'conv': conversation_id})
        messages_rows = self.cursor.fetchall()
        messages = []
        for message in messages_rows:
            additional = pickle.loads(bytes(message['message'])) if message['message'] is not None else None
            if message['type'] == 'media':
                messages.append(MediaMessage(message['message_text'], message['id'],
                                             datetime.datetime.fromtimestamp(message['timestamp']),
                                                message['conversation'], additional[0], additional[1], additional[2]))
            elif message['type'] == 'vcard':
                messages.append(VCardMessage(message['message_text'], message['id'],
                                             datetime.datetime.fromtimestamp(message['timestamp']),
                                                message['conversation'], additional[0]))
            elif message['type'] == 'location':
                messages.append(LocationMessage(message['message_text'], message['id'],
                                                datetime.datetime.fromtimestamp(message['timestamp']),
                                                   message['conversation'], additional[0], additional[1]))
            else:
                messages.append(Message(message['message_text'], message['id'],
                                        datetime.datetime.fromtimestamp(message['timestamp']),
                                                       message['conversation']))
        return messages

    def open(self):
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))

    def close(self):
        self.connection.commit()
        self.connection.close()
        logger.info('Closed connection to database {}'.format(self.db_filename))

    def clear(self):
        logger.warn('Deleting everything from db {}'.format(self.db_filename))
        self.cursor.execute('DROP TABLE IF EXISTS users')
        self.cursor.execute('DROP TABLE IF EXISTS conversations')
        self.cursor.execute('DROP TABLE IF EXISTS messages')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (user TEXT UNIQUE, whatsapp_id TEXT UNIQUE)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS conversations (id INTEGER NOT NULL UNIQUE, user TEXT, participant TEXT)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS messages (id TEXT UNIQUE, conversation INTEGER NOT NULL, sender TEXT, timestamp INTEGER NOT NULL, type INTEGER NOT NULL, message_text TEXT, message BLOB)')
        self.connection.commit()
