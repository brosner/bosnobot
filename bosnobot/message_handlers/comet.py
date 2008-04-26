
class CometHandler(object):
    """
    A message handler that sends messages to an Orbited comet server.
    """
    def process_message(self, message):
        print "comment handler:", message
