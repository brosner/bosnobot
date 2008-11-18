
from twisted.internet import reactor

class Channel(object):
    """
    Represents an IRC channel.
    """
    def __init__(self, name):
        self.name = name
        self.joined = False
    
    def __repr__(self):
        return "<Channel: %s>" % self.name
    
    def msg(self, message, call_from_thread=False):
        """
        Tell the bot to send a message to this channel.
        """
        if call_from_thread:
            reactor.callFromThread(self.protocol.msg, self.name, message)
        else:
            self.protocol.msg(self.name, message)
    
    def me(self, message, call_from_thread=False):
        """
        Tell the bot to send a me action to this channel.
        """
        if call_from_thread:
            reactor.callFromThread(self.protocol.me, self.name, message)
        else:
            self.protocol.me(self.name, message)
    