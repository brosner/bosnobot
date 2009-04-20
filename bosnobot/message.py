
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
            message = self.queue.get()
            if message == "stop":
                break
            for handler in self.handlers:
                handler.process_message(message)
        log.msg("Stopping message dispatch thread.", logLevel=logging.DEBUG)

class MessageDispatcher(object):
    """
    Handles the dispatching of message to the message handlers
    """
    dispatcher_thread_class = MessageDispatcherThread
    
    def __init__(self):
        self.queue = Queue()
        self.thread = self.dispatcher_thread_class(self.queue)
        self.thread.start()
    
    def dispatch(self, message):
        """
        Takes the given message and puts it on the queue for dispatching.
        """
        self.queue.put(message)
    
    def stop(self):
        """
        Stops the message dispatcher.
        """
        self.queue.put("stop")

class Message(object):
    """
    Represents a message sent over IRC.
    """
    def __init__(self, user, channel, message, **kwargs):
        self.user = user
        self.nickname = user.split("!", 1)[0]
        self.channel = channel
        self.message = message
        # @@@ hack for now
        self.action = kwargs.pop("action", False)
    
    def __str__(self):
        return self.message
