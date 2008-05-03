
from datetime import datetime
from cStringIO import StringIO

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, mapper, relation
from bosnobot.conf import settings
from bosnobot.channel import Channel
from bosnobot.message import Message

class DatabaseLogger(object):
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URI,
            echo=getattr(settings, "DATABASE_ECHO", False))
        self.metadata = MetaData(bind=self.engine)
        self.setup_tables()
        self.session = sessionmaker(bind=self.engine)()
    
    def setup_tables(self):
        channels_table = Table("irc_channel", self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)))
        mapper(Channel, channels_table, properties={
            "messages": relation(Message, backref="channel"),
        })
        
        messages_table = Table("irc_message", self.metadata,
            Column("id", Integer, primary_key=True),
            Column("channel_id", ForeignKey("irc_channel.id")),
            Column("nickname", String(19)),
            Column("text", Text),
            Column("logged", DateTime, default=datetime.now),
            Column("is_action", Boolean),
            Column("is_blocked", Boolean))
        mapper(Message, messages_table, properties={
            "message": messages_table.c.text,
        })
        
        # setup tables
        self.metadata.create_all()
    
    def as_sql(self):
        buf = StringIO()
        def buffer_output(s, p=""):
            return buf.write(s + p)
        engine = create_engine(settings.DATABASE_URI,
            strategy="mock",
            executor=buffer_output)
        self.metadata.create_all(engine)
        print buf.getvalue()
        
    def process_message(self, message):
        self.session.save(message)
        self.session.commit()
