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
import mysql.connector
# import sqlite3

from . import Config as config
from .DataLoader import DataLoader


class MySQLCalendarLoader(DataLoader):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def getDBDir(self):
        dbDir = os.getenv('DB_DIR', None)
        if dbDir is None:
            dbDir = os.path.join(config.getParentDir(), 'db')

        return dbDir

    def makeConnection(self):
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', "127.0.0.1"),
            port=os.getenv('DB_PORT', 3306),
            user=os.getenv('DB_UID', 'your login id'),
            password=os.getenv('DB_PWD', "your password"),
            database=os.getenv('DB_NAME', 'quantlib'))

        return conn

    def load(self, calName):
        conn = self.makeConnection()
        params = (calName,)
        c = conn.cursor()
        recs = c.execute('SELECT date FROM calendars WHERE calCode=%s', params)
        dates = [int(d[0]) for d in recs]
        conn.close()

        return dates
