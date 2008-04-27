
from pyorbited.simple import Client

class CometHandler(object):
    """
    A message handler that sends messages to an Orbited comet server.
    """
    def __init__(self):
        self.orbited = Client()
        self.orbited.connect()
    
    def process_message(self, message):
        print "[comet]: received %r" % message
        self.orbited.event(["user, 0, /demo"], str(message), False)
