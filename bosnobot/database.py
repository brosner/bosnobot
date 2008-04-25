
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper, relation

from bosnobot.conf import settings

engine = create_engine(settings.DATABASE_URI, echo=True)
metadata = MetaData(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

class Message(object):
    __table__ = Table("irc_message", metadata, autoload=True)
mapper(Message, Message.__table__)

class Channel(object):
    __table__ = Table("irc_channel", metadata, useexisting=True)
mapper(Channel, Channel.__table__, properties={
    "messages": relation(Message, backref="channel"),
})
