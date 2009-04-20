
from datetime import datetime
from cStringIO import StringIO

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, mapper, relation
from sqlalchemy.sql import select
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
        self.channels_table = Table("irc_channel", self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
        )
        
        self.messages_table = Table("irc_message", self.metadata,
            Column("id", Integer, primary_key=True),
            Column("channel_id", Integer, ForeignKey("irc_channel.id"), nullable=False),
            Column("nickname", String(19)),
            Column("text", Text),
            Column("logged", DateTime, default=datetime.now),
            Column("is_action", Boolean, default=False),
            Column("is_blocked", Boolean, default=False),
        )
        
        # setup tables
        self.metadata.create_all()
            
    def process_message(self, message):
        channels, messages = self.channels_table, self.messages_table
        conn = self.engine.connect()
        
        s = select([channels], channels.c.name == message.channel.name)
        row = conn.execute(s).fetchone()
        if not row:
            ins = channels.insert().values(name=message.channel.name)
            result = conn.execute(ins)
            channel_id = result.last_inserted_ids()[0]
        else:
            channel_id = row["id"]
        
        ins = messages.insert().values(**{
            "nickname": message.nickname,
            "channel_id": channel_id,
            "text": message.message,
            "logged": datetime.now(),
            "is_action": message.action,
        })
        conn.execute(ins)
