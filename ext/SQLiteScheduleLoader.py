# Copyright (C) 2019 Wenhua Wang
#
# This file is part of QuantLibExt, which is an extension to the
# free-software/open-source quantitative library QuantLib - http://quantlib.org/
#
# QuantLibExt is free software: you can redistribute it and/or modify it
# under the terms of the BSD license.
#
# QuantLib's license is at <http://quantlib.org/license.shtml>.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the license for more details.


import os
import sqlite3
# import json

from . import Config as config
from .DataLoader import DataLoader


class SQLiteScheduleLoader(DataLoader):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def getDBDir(self):
        dbDir = os.getenv('DB_DIR', None)
        if dbDir is None:
            dbDir = os.path.join(config.getParentDir(), 'db')

        return dbDir

    def makeConnection(self):
        dbPath = os.path.join(self.getDBDir(), 'quantlib.db')
        conn = sqlite3.connect(dbPath)

        return conn

    def load(self, prodCode):
        conn = self.makeConnection()
        params = (prodCode,)
        c = conn.cursor()
        # https://docs.python.org/3/library/sqlite3.html
        c.execute(
            """SELECT rolling, calendar
               FROM schedules
               WHERE prodCode=?""", params)
        rec = c.fetchone()
        if rec is None:
            raise RuntimeError("schedue for %s was not found" % prodCode)
        c.execute(
            """SELECT date
               FROM schedule_dates
               WHERE prodCode=?""", params)
        rows = c.fetchall()

        # schedule = json.loads(rec[0])
        # conn.close()

        schedule = {
            'prodCode': prodCode,
            'rolling': rec[0],
            'calendar': rec[1],
            'dates': [dt[0] for dt in rows]
        }

        return schedule
