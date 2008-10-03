
import logging
import threading

from Queue import Queue
from twisted.python import log

from bosnobot.conf import settings

class EventDispatcherThread(threading.Thread):
    """
    The default event dispatch thread that pulls from the dispatch queue and
    passes to the event handlers.
    """
    def __init__(self, queue):
        self.queue = queue
        self.handlers = []
        super(EventDispatcherThread, self).__init__()
    
    def _initialize(self):
        """
        Initializes the event handlers to be used.
        """
        log.msg("Initializing event handlers", logLevel=logging.DEBUG)
        for handler in settings.EVENT_HANDLERS:
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
            event = self.queue.get()
            if event == "stop":
                break
            for handler in self.handlers:
                handler.process_event(event)
        log.msg("Stopping event dispatch thread.", logLevel=logging.DEBUG)

class EventDispatcher(object):
    """
    Handles the dispatching of event to the event handlers
    """
    dispatcher_thread_class = EventDispatcherThread
    
    def __init__(self):
        self.queue = Queue()
        self.thread = self.dispatcher_thread_class(self.queue)
        self.thread.start()
    
    def dispatch(self, event):
        """
        Takes the given event and puts it on the queue for dispatching.
        """
        self.queue.put(event)
    
    def stop(self):
        """
        Stops the event dispatcher.
        """
        self.queue.put("stop")

class Event(object):
    pass
