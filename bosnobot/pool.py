
class ChannelPool(object):
    """
    Handles a pool of IRC channels that the bot will use.
    """
    def __init__(self, channels={}):
        for channel in channels:
            self.add(channel)
