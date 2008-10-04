
import time

from bosnobot.channel import Channel

class ChannelPool(object):
    """
    Handles a pool of IRC channels that the bot will use.
    """
    def __init__(self, protocol):
        self.channels = {}
        self.protocol = protocol
    
    def __iter__(self):
        """
        An iterator for the ChannelPool.
        """
        for channel in self.channels.itervalues():
            yield channel
    
    def __getitem__(self, channel):
        return self.channels[channel.lower()]
    
    def get(self, channel):
        """
        Get a channel from the pool failing silently.
        """
        try:
            return self[channel.lower()]
        except KeyError:
            return None
    
    def join(self, channel):
        """
        Joins a channel and adds to the pool.
        """
        self.channels[channel.name.lower()] = channel
        channel.protocol = self.protocol
        self.protocol.join(channel.name)
    
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
