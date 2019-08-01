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


from . import Config as config
from . import Utils as utils


class CalendarIndex:
    class __CalendarIndex:
        def __init__(self):
            self.calIndex = {}

            url = config.getCalendarIndexURL()
            reader = utils.loadCSVFromUrl(url)
            # skip the first two rows
            next(reader)
            next(reader)
            for row in reader:
                self.calIndex[row[0].strip().upper()] = (
                    row[1].strip(), row[2].strip())

        def getIndex(self):
            return self.calIndex

        def getCalInfo(self, calName):
            return self.calIndex.get(calName)

        def getUrl(self, calName):
            calInfo = self.calIndex.get(calName)
            if calInfo is None:
                raise RuntimeError(
                    "Information for %s was not found" % calName)
            else:
                return calInfo[1]

        def __str__(self):
            return repr(self) + ' Calendar Index'

    instance = None

    def __init__(self):
        if not CalendarIndex.instance:
            CalendarIndex.instance = CalendarIndex.__CalendarIndex()

    def __getattr__(self, name):
        return getattr(self.instance, name)
