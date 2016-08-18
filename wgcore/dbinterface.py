import logging
import sqlite3

logger = logging.getLogger(__name__)

class DBInterface:
    def __init__(self):
        self.db_filename = 'user_data.db'
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (user TEXT UNIQUE, whatsapp_id TEXT UNIQUE)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS conversations (id TEXT UNIQUE, user TEXT, participant TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS messages (id TEXT UNIQUE, conversation TEXT,'
                            'from TEXT, timestamp INT NOT NULL, type INT NOT NULL, message TEXT)')
        self.connection.commit()
        self.connection.close()

    def add_user(self, user_id, whatsapp_id):
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))
        
        self.cursor = self.connection.cursor()
        self.cursor.execute('INSERT INTO users VALUES (:user, :whatsapp)', {'user': user_id, 'whatsapp': whatsapp_id})
        
        self.connection.commit()
        logger.info('Commiting changes to database {}. User {} added'.format(self.db_filename, user_id))
        self.connection.close()

    def add_conversation(self, user_id, participant):
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))
        
        self.cursor = self.connection.cursor()
        self.cursor.execute('INSERT INTO conversations VALUES (:user, :part)', {'user': user_id, 'part': participant})
        
        self.connection.commit()
        logger.info('Commiting changes to database {}. Conversation {} added'.format(self.db_filename, user_id))
        self.connection.close()

    def add_message(self, conversation_id, message):
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))

        self.cursor = self.connection.cursor()
        # TODO

        self.connection.commit()
        # logger.info('Commiting changes to database {}. Message {} added'.format(self.db_filename, message))
        self.connection.close()

    def get_conversations(self, user_id):
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))
        
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT id, participant FROM conversations WHERE user = :user', {'user': user_id})
        convs = self.cursor.fetchall()
        self.connection.close()
        return convs

    def get_conversation(self, user_id, participant):
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))
        
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT id, participant FROM conversations WHERE user = :user AND participant = :part',
                            {'user': user_id, 'part': participant})
        conv = self.cursor.fetchone()
        self.connection.close()
        return conv

    def get_messages(self, conversation_id):
        self.connection = sqlite3.connect(self.db_filename)
        logger.info('Connected to database {}'.format(self.db_filename))

        self.cursor = self.connection.cursor()
        # TODO
        messages = self.cursor.fetchall()
        self.connection.close()
        return messages
