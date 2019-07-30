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

        def getLoader(self):
            return self.loader

        def __str__(self):
            return repr(self) + 'Impl of CalendarManager'

    instance = None

    def __init__(self, loader=None):
        if not CalendarManager.instance:
            CalendarManager.instance = CalendarManager.__CalendarManager(
                loader)

    def __getattr__(self, name):
        return getattr(self.instance, name)

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


def getCalendar(calName):
    calMgr = CalendarManager()
    if calMgr is None:
        print('.... calMgr is None ...')
    cal = calMgr.getCalendar(calName)
    # print('xxxxx ', type(cal), cal)
    return cal
