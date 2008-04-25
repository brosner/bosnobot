
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from bosnobot.database import session
from bosnobot.database import Channel, Message

class IrcBot(irc.IRCClient):
    nickname = "ihatethaub"
    
    def signedOn(self):
        # once signed on to the irc server join each channel.
        for channel in self.factory.channels:
            self.join(channel)
    
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
