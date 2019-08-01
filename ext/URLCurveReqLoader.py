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
from .DataLoader import DataLoader


class URLCurveReqLoader(DataLoader):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def load(self, curveId):
        filePath = config.getCurveInputFile(curveId + '.json')
        instFileUrl = 'file:///' + filePath

        req = utils.loadJsonFromUrl(instFileUrl)

        return req
