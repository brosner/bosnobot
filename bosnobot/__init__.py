
from twisted.internet import reactor

from bosnobot.bot import IrcBotFactory

if __name__ == "__main__":
    factory = IrcBotFactory(["#djangobot"])
    reactor.connectTCP("irc.freenode.net", 6667, factory)
    reactor.run()
