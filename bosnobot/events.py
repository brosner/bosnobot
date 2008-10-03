
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
    
    def as_dict(self):
        return {
            "kind": "message",
            "nickname": self.nickname,
            "channel": self.channel.name,
            "message": self.message,
        }

class UserJoined(object):
    def __init__(self, user, channel):
        self.user = user
        self.nickname = user.split("!", 1)[0]
        self.channel = channel
    
    def __str__(self):
        return "%s joined %s" % (self.nickname, self.channel)
    
    def as_dict(self):
        return {
            "kind": "join",
            "nickname": self.nickname,
            "channel": self.channel.name,
        }

class UserLeft(object):
    def __init__(self, user, channel):
        self.user = user
        self.nickname = user.split("!", 1)[0]
        self.channel = channel
    
    def __str__(self):
        return "%s left %s" % (self.nickname, self.channel)
    
    def as_dict(self):
        return {
            "kind": "leave",
            "nickname": self.nickname,
            "channel": self.channel.name,
        }

class UserQuit(object):
    def __init__(self, user, message):
        self.user = user
        self.nickname = user.split("!", 1)[0]
        self.message = message
    
    def __str__(self):
        return "%s left (%s)" % (self.nickname, self.message)
    
    def as_dict(self):
        return {
            "kind": "quit",
            "nickname": self.nickname,
            "message": self.message
        }

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
    
    def as_dict(self):
        return {
            "kind": "kick",
            "kickee": self.kickee,
            "channel": self.channel.name,
            "kicker": self.kicker,
            "messgae": self.message,
        }
