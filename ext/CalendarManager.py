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
from . import DatetimeUtils as dfs
from .URLCalendarLoader import URLCalendarLoader
from .CalendarIndex import CalendarIndex


class CalendarManager:
    class __CalendarManager:
        def __init__(self, loader=None):
            self.calCache = {}
            if loader is None:
                self.loader = URLCalendarLoader()
            else:
                self.loader = loader

        def setLoader(self, loader):
            self.loader = loader

        def getLoader(self):
            return self.loader

        def buildCustomCalendar(self, calName):
            cal = ql.BespokeCalendar(calName)
            cal.addWeekend(ql.Saturday)
            cal.addWeekend(ql.Sunday)
            days = self.loader.load(calName)
            for day in days:
                cal.addHoliday(dfs.toQLDate(int(day)))

            return cal

        def initBuiltCalendar(self, calInfo):
            tmp = calInfo.split('.')
            if len(tmp) > 1:
                clazz, cal = tmp
            else:
                cal = None
                clazz = tmp[0]

            clazz = getattr(ql, clazz)
            if cal is None:
                calc = clazz()
            else:
                calc = clazz(getattr(clazz, cal))

            return calc

        def getCalendar(self, calName):
            if isinstance(calName, ql.Calendar):
                return calName

            # calName = str(calName)
            calName = calName.upper()
            if calName in self.calCache:
                return self.calCache[calName]

            calIndex = CalendarIndex()
            calInfo = calIndex.getCalInfo(calName)
            if calInfo is None:
                raise RuntimeError(
                    "Calendar %s was not found, please check Calendar.idx ..." % calName)

            if calInfo[0] is None and calInfo[1] is None:
                return None

            cal = None
            if calInfo[1] is not None and len(calInfo[1].strip()) > 0:
                cal = self.buildCustomCalendar(calName)
            else:
                cal = self.initBuiltCalendar(calInfo[0])

            if cal is not None:
                self.calCache[calName] = cal

            return cal

        def __str__(self):
            return repr(self) + 'Impl of CalendarManager'

    instance = None

    def __init__(self, loader=None):
        if not CalendarManager.instance:
            CalendarManager.instance = CalendarManager.__CalendarManager(
                loader)
        elif loader is not None:
            CalendarManager.instance.setLoader(loader)

    def __getattr__(self, name):
        return getattr(self.instance, name)


def setLoader(loader):
    _ = CalendarManager(loader)


def getCalendar(calName):
    calMgr = CalendarManager()
    cal = calMgr.getCalendar(calName)
    return cal
