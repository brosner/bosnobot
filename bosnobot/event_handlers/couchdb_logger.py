
import couchdb
import datetime

from bosnobot.message import Message

class CouchDBLogger(object):
    def __init__(self):
        self.server = couchdb.Server("http://127.0.0.1:5984/")
        self.database = self.server["irc_events"]
    
    def process_event(self, event):
        document = couchdb.Document(**dict(event.as_dict(), **{
            "logged": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }))
        self.database.create(document)
