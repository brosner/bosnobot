
class ChannelPool(object):
    """
    Handles a pool of IRC channels that the bot will use.
    """
    def __init__(self, channels=[]):
        for channel in channels:
            self.add(channel)
    
    def __iter__(self):
        for channel in self.channels.itervalues():
            yield channel
    
    def add(self, channel):
        # use a dict to speed up lookups
        self.channels[channel.name] = channel
