
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

class UserJoined(object):
    def __init__(self, user, channel):
        self.user = user
        self.nickname = user.split("!", 1)[0]
        self.channel = channel
    
    def __str__(self):
        return "%s joined %s" % (self.nickname, self.channel)

class UserLeft(object):
    def __init__(self, user, channel):
        self.user = user
        self.nickname = user.split("!", 1)[0]
        self.channel = channel
    
    def __str__(self):
        return "%s left %s" % (self.nickname, self.channel)

class UserKicked(object):
    def __init__(self, kickee, channel, kicker, message):
        self.kickee = kickee
        self.channel = channel
        self.kicker = kicker
        self.message = message
    
    def __str__(self):
        return "%s was kicked from %s by %s (%s)" % (
            self.kickee, self.channel, self.kicker, self.message,
        )
