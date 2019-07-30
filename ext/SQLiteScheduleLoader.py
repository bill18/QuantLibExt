import os
import sqlite3
import json

from . import Config as config
from .ScheduleLoader import ScheduleLoader


class SQLiteScheduleLoader(ScheduleLoader):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def getDBDir(self):
        dbDir = os.getenv('DB_DIR', None)
        if dbDir is None:
            dbDir = os.path.join(config.getParentDir(), 'db')

        return dbDir

    def makeConnection(self):
        dbPath = os.path.join(self.getDBDir(), 'schedule.db')
        conn = sqlite3.connect(dbPath)

        return conn

    def load(self, prodCode):
        conn = self.makeConnection()
        params = (prodCode,)
        c = conn.cursor()
        # https://docs.python.org/3/library/sqlite3.html
        c.execute(
            'SELECT schedule FROM schedules WHERE prodCode=?', params)
        rec = c.fetchone()
        if rec is None:
            raise RuntimeError("schedue for %s was not found" % prodCode)
        schedule = json.loads(rec[0])
        conn.close()

        return schedule
