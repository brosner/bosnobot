
import threading

from Queue import Queue

from bosnobot.conf import settings

class MessageDispatcherThread(threading.Thread):
    """
    The default message dispatch thread that pulls from the dispatch queue and
    passes to the message handlers.
    """
    def __init__(self, queue):
        self.queue = queue
        self.handlers = []
        super(MessageDispatcherThread, self).__init__()
    
    def _initialize(self):
        """
        Initializes the message handlers to be used.
        """
        print "initializing message handlers"
        for handler in settings.MESSAGE_HANDLERS:
            bits = handler.split(".")
            module_name = ".".join(bits[:-1])
            try:
                mod = __import__(module_name, {}, {}, [""])
            except ImportError, e:
                print "unable to import %s: %s" % (handler, e)
            else:
                print "imported %s" % handler
                handler_class = getattr(mod, bits[-1])
                self.handlers.append(handler_class())
    
    def run(self):
        self._initialize()
        while True:
            message = self.queue.get()
            for handler in self.handlers:
                handler.process_message(message)

class MessageDispatcher(object):
    """
    Handles the dispatching of message to the message handlers
    """
    dispatcher_thread = MessageDispatcherThread
    
    def __init__(self):
        self.queue = Queue()
        self.thread = self.dispatcher_thread(self.queue)
        self.thread.start()
    
    def dispatch(self, message):
        """
        Takes the given message and puts it on the queue for dispatching.
        """
        self.queue.put(message)

class Message(object):
    """
    Represents a message sent over IRC.
    """
    def __init__(self, user, channel, message, bot):
        self.user = user
        self.channel = channel
        self.message = message
        self.bot = bot
