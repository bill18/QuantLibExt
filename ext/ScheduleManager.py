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

import QuantLib as ql
from . import QuantLibClassExt as qlx

from .URLScheduleLoader import URLScheduleLoader


class ScheduleManager:
    class __ScheduleManager:
        def __init__(self, loader=None):
            self.scheduleCache = {}
            if loader is None:
                self.loader = URLScheduleLoader()
            else:
                self.loader = loader

        def setLoader(self, loader):
            self.loader = loader

        def getLoader(self):
            return self.loader

        def createSchedule(self, prodId):
            data = self.loader.load(prodId)
            # print(data)
            schedule = qlx.Schedule(
                data["dates"], data["calendar"], data["rolling"], data["term_rolling"], data["tenor"], None, False)
            return schedule

        def getSchedule(self, prodId):
            if isinstance(prodId, ql.Schedule):
                return prodId

            prodId = prodId.upper()
            if prodId in self.scheduleCache:
                return self.scheduleCache[prodId]

            schedule = self.createSchedule(prodId)

            if schedule is not None:
                self.scheduleCache[prodId] = schedule

            return schedule

        def __str__(self):
            return repr(self) + 'Impl of ScheduleManager'

    instance = None

    def __init__(self, loader=None):
        if not ScheduleManager.instance:
            ScheduleManager.instance = ScheduleManager.__ScheduleManager(
                loader)
        elif loader is not None:
            ScheduleManager.instance.setLoader(loader)

    def __getattr__(self, name):
        return getattr(self.instance, name)


def setLoader(loader):
    _ = ScheduleManager(loader)


def getSchedule(prodId):
    mgr = ScheduleManager()
    return mgr.getSchedule(prodId)
