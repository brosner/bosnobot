
import logging

from twisted.python import log
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from bosnobot.conf import settings
from bosnobot.pool import ChannelPool
from bosnobot.channel import Channel
from bosnobot.event import EventDispatcher
from bosnobot import events
from bosnobot.message import Message

class IrcProtocol(irc.IRCClient):
    channel_pool_class = ChannelPool
    
    def connectionMade(self):
        self.channel_pool = self.channel_pool_class(self)
        self.nickname = settings.BOT_NICKNAME
        self.password = settings.BOT_PASSWORD
        irc.IRCClient.connectionMade(self)
        self._initialize_bot()
    
    def connectionLost(self, reason):
        log.msg("Connection lost")
        self.bot.shutdown()
    
    def _initialize_bot(self):
        if self.factory.bot_path is None:
            self.bot = IrcBot(self)
            log.msg("Loaded default bot")
        else:
            bits = self.factory.bot_path.split(".")
            module_name = ".".join(bits[:-1])
            try:
                mod = __import__(module_name, {}, {}, [""])
            except ImportError, e:
                log.msg("Unable to import %s: %s" % (self.factory.bot_path, e))
            else:
                bot_class = getattr(mod, bits[-1])
                self.bot = bot_class(self)
                log.msg("Loaded %s" % self.factory.bot_path)
    
    def signedOn(self):
        # once signed on to the irc server join each channel.
        for channel in self.bot.channels:
            self.channel_pool.join(channel)
        self.bot.initialize()
    
    def joined(self, channel):
        channel = self.channel_pool.get(channel)
        channel.joined = True
        log.msg("joined %s" % channel.name)
    
    def privmsg(self, user, channel, msg):
        if self.channel_pool.joined_all:
            channel = self.channel_pool.get(channel)
            event = events.Message(user, channel, msg)
            self.factory.event_dispatcher.dispatch(event)
    
    def userJoined(self, user, channel):
        if self.channel_pool.joined_all:
            channel = self.channel_pool.get(channel)
            event = events.UserJoined(user, channel)
            self.factory.event_dispatcher.dispatch(event)
    
    def userLeft(self, user, channel):
        if self.channel_pool.joined_all:
            channel = self.channel_pool.get(channel)
            event = events.UserLeft(user, channel)
            self.factory.event_dispatcher.dispatch(event)
    
    def userKicked(self, kickee, channel, kicker, message):
        if self.channel_pool.joined_all:
            channel = self.channel_pool.get(channel)
            event = events.UserKicked(kickee, channel, kicker, message)
            self.factory.event_dispatcher.dispatch(event)

class IrcBot(object):
    def __init__(self, protocol):
        self.protocol = protocol
        self.channels = []
        for channel in settings.BOT_CHANNELS:
            self.channels.append(Channel(channel))
    
    def initialize(self):
        pass
    
    def shutdown(self):
        pass

class IrcBotFactory(protocol.ClientFactory):
    protocol = IrcProtocol
    event_dispatcher_class = EventDispatcher
    
    def __init__(self, bot_path, channels):
        self.bot_path = bot_path
        self.channels = channels
    
    def clientConnectionFailed(self, connector, reason):
        log.msg("connection failed: %s" % reason)
        reactor.stop()
    
    def startFactory(self):
        self.event_dispatcher = self.event_dispatcher_class()
    
    def stopFactory(self):
        self.event_dispatcher.stop()
