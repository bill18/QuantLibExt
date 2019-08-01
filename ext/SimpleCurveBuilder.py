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
from . import DatetimeUtils as dtu
from . import QuantLibClassExt as qlx
from . import Config as config
from . import Utils as utils


def ZeroCurve(asOfDate, curveId):
    filePath = config.getCurveInputFile(curveId + '.json')
    instFileUrl = 'file:///' + filePath

    insts = utils.loadJsonFromUrl(instFileUrl)
    ql.Settings.instance().evaluationDate = dtu.toQLDate(asOfDate)
    dates = [rec[0] for rec in insts['marks']]
    rates = [rec[1] for rec in insts['marks']]
    curve = qlx.ZeroCurve(dates, rates, insts['basis'],
                          insts['calendar'], insts['interpolation'], insts['compounding'], insts['frequency'])
    return curve


def DiscountCurve(asOfDate, curveId):
    filePath = config.getCurveInputFile(curveId + '.json')
    instFileUrl = 'file:///' + filePath

    insts = utils.loadJsonFromUrl(instFileUrl)
    ql.Settings.instance().evaluationDate = dtu.toQLDate(asOfDate)
    dates = [rec[0] for rec in insts['marks']]
    rates = [rec[1] for rec in insts['marks']]
    curve = qlx.DiscountCurve(dates, rates, insts['basis'],
                              insts['calendar'], insts['interpolation'], insts['compounding'], insts['frequency'])
    return curve


def ForwardCurve(asOfDate, curveId):
    filePath = config.getCurveInputFile(curveId + '.json')
    instFileUrl = 'file:///' + filePath

    insts = utils.loadJsonFromUrl(instFileUrl)
    ql.Settings.instance().evaluationDate = dtu.toQLDate(asOfDate)
    dates = [rec[0] for rec in insts['marks']]
    rates = [rec[1] for rec in insts['marks']]
    curve = qlx.ForwardCurve(dates, rates, insts['basis'],
                             insts['calendar'], insts['interpolation'], insts['compounding'], insts['frequency'])
    return curve
