
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from bosnobot.conf import settings
from bosnobot.pool import ChannelPool
from bosnobot.channel import Channel
from bosnobot.message import Message

class IrcBot(irc.IRCClient):
    nickname = settings.BOT_NICKNAME
    channel_pool = ChannelPool
    
    def __init__(self):
        self.channel_pool = self.channel_pool(self)
    
    def signedOn(self):
        # once signed on to the irc server join each channel.
        for channel in self.factory.channels:
            self.channel_pool.join(channel)
    
    def joined(self, channel):
        pass
    
    def privmsg(self, user, channel, msg):
        print repr((user, channel, msg))

class IrcBotFactory(protocol.ClientFactory):
    protocol = IrcBot
    
    def __init__(self, channels):
        self.channels = channels
    
    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()
