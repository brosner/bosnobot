
import sys
import threading

from twisted.python import log
from twisted.internet import reactor

from bosnobot.conf import settings
from bosnobot.bot import IrcBotFactory

factory = IrcBotFactory(settings.BOT_CHANNELS)

def main_loop():
    reactor.connectTCP(settings.BOT_IRC_SERVER, settings.BOT_IRC_PORT, factory)
    reactor.run()

def main():
    log.startLogging(sys.stdout)
    main_loop()

if __name__ == "__main__":
    main()
