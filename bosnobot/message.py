
import logging
import threading

from Queue import Queue
from twisted.python import log

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
        log.msg("Initializing message handlers", logLevel=logging.DEBUG)
        for handler in settings.MESSAGE_HANDLERS:
            bits = handler.split(".")
            module_name = ".".join(bits[:-1])
            try:
                mod = __import__(module_name, {}, {}, [""])
            except ImportError, e:
                log.msg("Unable to import %s: %s" % (handler, e))
            else:
                handler_class = getattr(mod, bits[-1])
                self.handlers.append(handler_class())
                log.msg("Loaded %s" % handler)
    
    def run(self):
        self._initialize()
        while True:
            obj = self.queue.get()
            if obj == "stop":
                break
            message, bot = obj
            for handler in self.handlers:
                handler.process_message(message, bot)
        log.msg("Stopping message dispatch thread.", logLevel=logging.DEBUG)

class MessageDispatcher(object):
    """
    Handles the dispatching of message to the message handlers
    """
    dispatcher_thread = MessageDispatcherThread
    
    def __init__(self):
        self.queue = Queue()
        self.thread = self.dispatcher_thread(self.queue)
        self.thread.start()
    
    def dispatch(self, message, bot):
        """
        Takes the given message and puts it on the queue for dispatching.
        """
        self.queue.put((message, bot))
    
    def stop(self):
        """
        Stops the message dispatcher.
        """
        self.queue.put("stop")

class Message(object):
    """
    Represents a message sent over IRC.
    """
    def __init__(self, user, channel, message):
        self.user = user
        self.channel = channel
        self.message = message
    
    def __str__(self):
        return self.message
