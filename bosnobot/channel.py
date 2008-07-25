
from twisted.internet import reactor

class Channel(object):
    """
    Represents an IRC channel.
    """
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
        self.joined = False
    
    def __repr__(self):
        return "<Channel: %s>" % self.name
    
    def msg(self, message, call_from_thread=False):
        """
        Tell the bot to send a message to this channel.
        """
        if call_from_thread:
            reactor.callFromThread(self.bot.msg, self.name, message)
        else:
            self.bot.msg(self.name, message)
