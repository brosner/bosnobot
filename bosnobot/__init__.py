
import os
import sys
import logging
import threading

from twisted.python import log, usage
from twisted.internet import reactor
from twisted.application import internet

from bosnobot.conf import settings, ENVIRON_VARIABLE
from bosnobot.bot import IrcBotFactory
from bosnobot.log import PythonLoggingObserver

class Options(usage.Options):
    synopsis = "HELLO WORLD"
    optParameters = [["settings", "", None]]

class IrcBotService(internet.TCPClient):
    def __init__(self, *args, **kwargs):
        factory = IrcBotFactory(settings.BOT, settings.BOT_CHANNELS)
        internet.TCPClient.__init__(self,
            settings.BOT_IRC_SERVER, settings.BOT_IRC_PORT, factory)

def main_loop():
    factory = IrcBotFactory(settings.BOT, settings.BOT_CHANNELS)
    reactor.connectTCP(settings.BOT_IRC_SERVER, settings.BOT_IRC_PORT, factory)
    reactor.run()

def setup_logging():
    observer = PythonLoggingObserver()
    observer.start()
    # configure logging in python
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt = "%m-%d %H:%M")

def main():
    config = Options()
    config.parseOptions()
    if config["settings"]:
        os.environ[ENVIRON_VARIABLE] = config["settings"]
    setup_logging()
    main_loop()

if __name__ == "__main__":
    main()
