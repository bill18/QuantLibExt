import os
import sqlite3

from . import Config as config
from .CalendarLoader import CalendarLoader


class SQLiteCalendarLoader(CalendarLoader):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def getDBDir(self):
        dbDir = os.getenv('DB_DIR', None)
        if dbDir is None:
            dbDir = os.path.join(config.getParentDir(), 'db')

        return dbDir

    def makeConnection(self):
        dbPath = os.path.join(self.getDBDir(), 'cal.db')
        conn = sqlite3.connect(dbPath)

        return conn

    def load(self, calName):
        conn = self.makeConnection()
        params = (calName,)
        c = conn.cursor()
        recs = c.execute('SELECT date FROM calendars WHERE calCode=?', params)
        dates = [int(d[0]) for d in recs]
        conn.close()

        return dates
