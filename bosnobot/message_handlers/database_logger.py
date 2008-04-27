
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, mapper
from bosnobot.conf import settings
from bosnobot.message import Message

class DatabaseLogger(object):
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URI, echo=False)
        self.metadata = MetaData(bind=self.engine)
        self.setup_tables()
        self.session = sessionmaker(bind=self.engine)()
    
    def setup_tables(self):
        messages_table = Table("irc_message", self.metadata,
            Column("id", Integer, primary_key=True),
            Column("text", Text))
        mapper(Message, messages_table, properties={
            "message": messages_table.c.text,
        })
        
        # setup tables
        self.metadata.create_all()
        
    def process_message(self, message, bot):
        self.session.save(message)
        self.session.commit()
