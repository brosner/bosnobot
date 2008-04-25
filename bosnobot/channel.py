
class Channel(object):
    """
    Represents an IRC channel.
    """
    
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
    
    def msg(self, message):
        """
        Tell the bot to send a message to this channel.
        """
        self.bot.msg(self.name, message)
