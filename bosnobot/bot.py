
import logging

from twisted.python import log
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from bosnobot.conf import settings
from bosnobot.pool import ChannelPool
from bosnobot.channel import Channel
from bosnobot.message import MessageDispatcher, Message

class IrcBot(irc.IRCClient):
    channel_pool_class = ChannelPool
    nickname = settings.BOT_NICKNAME
    
    def __init__(self):
        self.channel_pool = self.channel_pool_class(self)
    
    def signedOn(self):
        # once signed on to the irc server join each channel.
        for channel in self.factory.channels:
            self.channel_pool.join(channel)
    
    def joined(self, channel):
        channel = self.channel_pool.get(channel)
        channel.joined = True
        log.msg("joined %s" % channel.name)
    
    def privmsg(self, user, channel, msg):
        if self.channel_pool.joined_all:
            channel = self.channel_pool.get(channel)
            self.factory.message_dispatcher.dispatch(Message(user, channel, msg))

class IrcBotFactory(protocol.ClientFactory):
    protocol = IrcBot
    message_dispatcher_class = MessageDispatcher
    
    def __init__(self, channels):
        self.channels = channels
    
    def clientConnectionFailed(self, connector, reason):
        log.msg("connection failed: %s" % reason)
        reactor.stop()
    
    def startFactory(self):
        self.message_dispatcher = self.message_dispatcher_class()
    
    def stopFactory(self):
        self.message_dispatcher.stop()
