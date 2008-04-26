
import threading

from twisted.internet import reactor

from bosnobot.conf import settings
from bosnobot.bot import IrcBotFactory

if __name__ == "__main__":
    factory = IrcBotFactory(settings.BOT_CHANNELS)
    reactor.connectTCP(settings.BOT_IRC_SERVER, settings.BOT_IRC_PORT, factory)
    reactor.run()
