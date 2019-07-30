import os

from . import Config as config
from . import Utils as utils
from .CalendarLoader import CalendarLoader
from .CalendarIndex import CalendarIndex


class URLCalendarLoader(CalendarLoader):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def load(self, calName):
        calIdx = CalendarIndex()
        calUrl = calIdx.getUrl(calName)
        if calUrl is None:
            raise RuntimeError("url is mandatory in URLCalendarLoader")
        if calUrl.startswith('file:') or calUrl.startswith('http:') or calUrl.startswith('https:'):
            url = calUrl
        else:
            url = 'file:///' + os.path.join(config.getCalendarDir(), calUrl)

        # res = utils.readFromUrl(url)
        # reader = utils.parseCSVString(res)
        res = utils.loadCSVFromUrl(url)
        dates = [int(d[0]) for d in res]

        return dates
