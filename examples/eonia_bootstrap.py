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

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import datetime
import ext.CurveBuilder as builder
# import ext.Config as config
import ext.CurveUtils as cutil


def plotCurve(dates, values, lineType='-', width=10, height=9):
    pydt = [datetime.datetime(d.year(), d.month(), d.dayOfMonth())
            for d in dates]
    fig, ax = plt.subplots()
    fig.set_size_inches(width, height)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda r, pos: '{:.2%}'.format(r)))
    plt.subplots_adjust(bottom=0.2)
    l, = plt.plot(pydt, values, lineType)
    plt.show()


if __name__ == '__main__':
    asOfDate = 20121211
    basis = 'Act/365F'

    curve = builder.PiecewiseLogCubicDiscountCurve(
        asOfDate, basis, 'eonia')

    data = cutil.oneDayForwardRates(curve, '2Y', 'TGT', compounding='Simple')
    dates = data['dates']
    rates = data['rates']

    plotCurve(dates, rates, '.')
