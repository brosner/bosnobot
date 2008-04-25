
class Message(object):
    """
    Represents a message sent over IRC.
    """
    
    def __init__(self, channel, message):
        self.channel = channel
        self.message = message
