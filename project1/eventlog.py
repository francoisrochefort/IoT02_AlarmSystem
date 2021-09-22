
import pymongo
from datetime import date, datetime


# misc. constants
MONGODB_URI = "localhost"
DATE_FORMAT = "%Y/%m/%d"
TIME_FORMAT = "%H:%M:%S"


class EventLog:
    """
    Used by the history window to list all event logs and
    by the alarm to write new events
    """

    def __init__(self):

        # use the good mongo database
        client = pymongo.MongoClient(MONGODB_URI)
        self.db = client.project1

    def write_event(self, object, event):
        """
        Write a new entry into the events collection
        of the project1 mongo database
        """
        return(self.db.events.insert_one({
            "date":  date.today().strftime(DATE_FORMAT),
            "time":  datetime.now().strftime(TIME_FORMAT),
            "object": object,
            "event": event,
        }).inserted_id)

    def get_event_logs(self):
        return self.db.events.find().sort([
            ['date', -1],
            ['time', -1]]).limit(10)
