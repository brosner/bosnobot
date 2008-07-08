
import time

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
    
    def __getitem__(self, channel):
        return self.channels[channel]
    
    def get(self, channel):
        """
        Get a channel from the pool failing silently.
        """
        try:
            return self[channel]
        except KeyError:
            return None
    
    def join(self, channel):
        """
        Joins a channel and adds to the pool.
        """
        self.channels[channel] = Channel(channel, self.bot)
        self.bot.join(channel)
    
    def _joined_all(self):
        """
        Returns True if all channels in the pool have been joined. Otherwise,
        return False.
        """
        if not self.channels:
            return False
        for channel in self:
            if not channel.joined:
                return False
        return True
    joined_all = property(_joined_all)
