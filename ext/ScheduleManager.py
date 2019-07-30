import QuantLib as ql
# from . import DatetimeUtils as dfs
# from . import QuantLibUtils as qlu
from . import QuantLibClassExt as qlx
# from . import CalendarManager as calMgr

from .URLScheduleLoader import URLScheduleLoader


class ScheduleManager:
    class __ScheduleManager:
        def __init__(self, loader=None):
            self.scheduleCache = {}
            if loader is None:
                self.loader = URLScheduleLoader()
            else:
                self.loader = loader

        def getLoader(self):
            return self.loader

        def __str__(self):
            return repr(self) + 'Impl of ScheduleManager'

    instance = None

    def __init__(self, loader=None):
        if not ScheduleManager.instance:
            ScheduleManager.instance = ScheduleManager.__ScheduleManager(
                loader)

    def __getattr__(self, name):
        return getattr(self.instance, name)

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


def getSchedule(prodId):
    mgr = ScheduleManager()
    return mgr.getSchedule(prodId)
