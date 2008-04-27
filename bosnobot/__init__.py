
import sys
import logging
import threading

from twisted.python import log
from twisted.internet import reactor

from bosnobot.conf import settings
from bosnobot.bot import IrcBotFactory

def main_loop():
    factory = IrcBotFactory(settings.BOT_CHANNELS)
    
    reactor.connectTCP(settings.BOT_IRC_SERVER, settings.BOT_IRC_PORT, factory)
    reactor.run()

def setup_logging():
    observer = log.PythonLoggingObserver()
    observer.start()
    # configure logging in python
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt = "%m-%d %H:%M")

def main():
    setup_logging()
    main_loop()

if __name__ == "__main__":
    main()
