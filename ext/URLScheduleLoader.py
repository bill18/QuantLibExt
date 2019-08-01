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
from .ScheduleLoader import ScheduleLoader


class URLScheduleLoader(ScheduleLoader):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.scheduleUrl = None

    def loadScheduleFile(self, prodId, url):
        if not (url.startswith('file:') or url.startswith('http:') or url.startswith('https:')):
            url = 'file:///' + url

        # content = utils.readFromUrl(url)
        # schedule = json.loads(content)
        # print("url:%s" % url)
        schedule = utils.loadJsonFromUrl(url)
        return schedule

    def getScheduleURL(self, prodId):
        url = config.getScheduleConfigURL()

        cfg = utils.loadJsonFromUrl(url)
        # cfg = json.loads(content)

        return cfg['URL']

    def load(self, prodId):
        prodId = prodId.upper()

        if self.scheduleUrl is None:
            self.scheduleUrl = self.getScheduleURL(prodId)

        if self.scheduleUrl is None or len(self.scheduleUrl) == 0:
            return None

        # print("URL pattern: " + scheduleUrl)
        url = self.scheduleUrl.format(prodId)
        # print("url=%s" % url)
        data = self.loadScheduleFile(prodId, url)
        # dates = [dfs.toQLDate(dt) for dt in data["dates"]]
        return data
