
import logging

from twisted.python import log
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from bosnobot.conf import settings
from bosnobot.pool import ChannelPool
from bosnobot.channel import Channel
from bosnobot.message import MessageDispatcher, Message

class IrcProtocol(irc.IRCClient):
    channel_pool_class = ChannelPool
    
    def lineReceived(self, line):
        # print line
        irc.IRCClient.lineReceived(self, line)
    
    def sendLine(self, line):
        # print "sending %s" % repr(line)
        irc.IRCClient.sendLine(self, line)
        
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
        self.dispatch_message(user, channel, msg)
    
    def action(self, user, channel, msg):
        # @@@ passing in as kwarg until event refactor is complete
        self.dispatch_message(user, channel, msg, action=True)
    
    def dispatch_message(self, user, channel, msg, **kwargs):
        if self.channel_pool.joined_all:
            channel = self.channel_pool.get(channel)
            message = Message(user, channel, msg, **kwargs)
            self.factory.message_dispatcher.dispatch(message)

class IrcBot(object):
    channels = []
    
    def __init__(self, protocol):
        self.protocol = protocol
        for channel in settings.BOT_CHANNELS:
            self.channels.append(Channel(channel))
    
    def initialize(self):
        pass
    
    def shutdown(self):
        pass

class IrcBotFactory(protocol.ClientFactory):
    protocol = IrcProtocol
    message_dispatcher_class = MessageDispatcher
    
    def __init__(self, bot_path, channels):
        self.bot_path = bot_path
        self.channels = channels
    
    def clientConnectionFailed(self, connector, reason):
        log.msg("connection failed: %s" % reason)
        reactor.stop()
    
    def startFactory(self):
        self.message_dispatcher = self.message_dispatcher_class()
    
    def stopFactory(self):
        self.message_dispatcher.stop()
