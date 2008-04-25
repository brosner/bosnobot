
from bosnobot.channel import Channel

class ChannelPool(object):
    """
    Handles a pool of IRC channels that the bot will use.
    """
    def __init__(self, bot):
        self.channels = {}
        self.bot = bot
    
    def __iter__(self):
        for channel in self.channels.itervalues():
            yield channel
    
    def join(self, channel):
        """
        Joins a channel and adds to the pool.
        """
        self.channels[channel] = Channel(channel, self.bot)
        self.bot.join(channel)
