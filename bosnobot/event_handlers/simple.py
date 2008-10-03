
import sys

from bosnobot.conf import settings

class FileLogger(object):
    def __init__(self):
        if settings.FILE_LOGGER_FILENAME == "stdout":
            self.stream = sys.stdout
        else:
            self.stream = open(settings.FILE_LOGGER_FILENAME)
    
    def process_event(self, event):
        self.stream.write(str(event))
        self.stream.write("\n")
        self.stream.flush()
