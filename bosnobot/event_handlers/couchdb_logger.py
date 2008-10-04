
import couchdb
import datetime

from bosnobot.message import Message

class CouchDBLogger(object):
    def __init__(self):
        self.server = couchdb.Server("http://127.0.0.1:5984/")
    
    def process_event(self, event):
        database = self.server["irc_events"]
        document = couchdb.Document(**dict(event.as_dict(), **{
            "logged": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }))
        database.create(document)
