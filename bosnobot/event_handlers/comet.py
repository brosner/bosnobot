
from pyorbited.simple import Client

class CometHandler(object):
    """
    A message handler that sends messages to an Orbited comet server.
    """
    def __init__(self):
        self.orbited = Client()
        self.orbited.connect()
    
    def process_event(self, event):
        print "[comet]: received %r" % event
        self.orbited.event(["user, 0, /demo"], str(event), False)
