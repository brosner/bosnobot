
class Message(object):
    """
    Represents a message sent over IRC.
    """
    def __init__(self, user, channel, message):
        self.user = user
        self.nickname = user.split("!", 1)[0]
        self.channel = channel
        self.message = message
    
    def __str__(self):
        return self.message
