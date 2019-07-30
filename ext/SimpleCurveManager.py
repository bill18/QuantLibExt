import QuantLib as ql
from . import DatetimeUtils as dtu
from . import QuantLibClassExt as qlx
from . import Config as config
from . import Utils as utils

# TODO: this has not been finished yet


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
