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

import QuantLib as ql
import ext.CurveBuilder as builder
# import ext.DatetimeUtils as dfs
import ext.CurveUtils as cutil

"""
http://mikejuniperhill.blogspot.com/2018/11/quantlib-python-builder-for-piecewise.html

"""


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


def plot(curve):
    today = curve.referenceDate()
    end = today + ql.Period(2, ql.Years)
    dates = [ql.Date(serial)
             for serial
             in range(today.serialNumber(), end.serialNumber() + 1)]

    rates = [curve.forwardRate(d,
                               ql.TARGET().advance(d, 1, ql.Days),
                               ql.Actual360(),
                               ql.Simple).rate()
             for d in dates]
    plotCurve(dates, rates)


def plot2(curve):
    today = curve.referenceDate()
    end = today + ql.Period(2, ql.Years)
    dates = [ql.Date(serial)
             for serial
             in range(today.serialNumber(), end.serialNumber() + 1)]

    rates_c = [curve.forwardRate(d,
                                 ql.TARGET().advance(d, 1, ql.Days),
                                 ql.Actual360(),
                                 ql.Simple).rate()
               for d in dates]
    pydt = [datetime.datetime(d.year(), d.month(), d.dayOfMonth())
            for d in dates]
    fig, ax = plt.subplots()
    fig.set_size_inches(10.5, 9.5)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda r, pos: '{:.2%}'.format(r)))
    plt.subplots_adjust(bottom=0.2)
    l, = plt.plot(pydt, rates_c, '.')
    plt.show()


def plot3(curve):
    today = curve.referenceDate()
    dates = [today + ql.Period(i, ql.Months) for i in range(0, 12 * 60 + 1)]
    rates = [curve.forwardRate(d, ql.TARGET().advance(d, 1, ql.Days),
                               ql.Actual360(), ql.Simple).rate()
             for d in dates]
    pydt = [datetime.datetime(d.year(), d.month(), d.dayOfMonth())
            for d in dates]
    fig, ax = plt.subplots()
    fig.set_size_inches(12.5, 10.5)
    l, = plt.plot(pydt, rates, '.', lw=2)
    plt.show()


def testPiecewiseLogCubicCurve(asOfDate, basis, curveId):
    curve = builder.PiecewiseLogCubicDiscountCurve(
        asOfDate, basis, curveId)
    today = curve.referenceDate()
    end = today + ql.Period(2, ql.Years)
    dates = [ql.Date(serial)
             for serial
             in range(today.serialNumber(), end.serialNumber() + 1)]

    rates = [curve.forwardRate(d,
                               ql.TARGET().advance(d, 1, ql.Days),
                               ql.Actual360(),
                               ql.Simple).rate()
             for d in dates]
    plotCurve(dates, rates, '.')


def testPiecewiseLogCubicCurveX(asOfDate, basis, curveId):
    curve = builder.PiecewiseLogCubicDiscountCurve(
        asOfDate, basis, curveId)
    # for node in curve.nodes():
    #     print(node)
    # today = curve.referenceDate()
    # end = today + ql.Period(2, ql.Years)
    # dates = [ql.Date(serial)
    #          for serial
    #          in range(today.serialNumber(), end.serialNumber() + 1)]

    # rates = [curve.forwardRate(d,
    #                            ql.TARGET().advance(d, 1, ql.Days),
    #                            'Act/360',
    #                            'Simple').rate()
    #          for d in dates]
    data = cutil.oneDayForwardRates(curve, '2Y', 'TGT', compounding='Simple')
    dates = data['dates']
    rates = data['rates']

    # test attribute forwarding with getattr in the wrapper
    print(curve.referenceDate())
    print(curve.dayCounter())
    print(curve.allowsExtrapolation())
    print(curve.disableExtrapolation())
    print(curve.maxDate())
    print(curve.maxTime())

    # case 1: QuantLib Date
    # maturity_dates = [ql.Date(24, 12, 2015), ql.Date(25, 2, 2016),
    #                   ql.Date(26, 5, 2016), ql.Date(10, 11, 2016),
    #                   ql.Date(30, 11, 2017), ql.Date(15, 11, 2018),
    #                   ql.Date(30, 11, 2020), ql.Date(30, 11, 2022),
    #                   ql.Date(15, 11, 2025)]

    # case 2: yyyymmdd
    maturity_dates = [
        20151224,
        20160225,
        20160526,
        20161110,
        20171130,
        20181115,
        20201130,
        20221130,
        20251115
    ]

    for d in maturity_dates:
        print("|%20s  %9.6f|" % (d, curve.discount(d)))

    plotCurve(dates, rates, '.')


def testPiecewiseCubicZeroCurve(asOfDate, basis, curveId):
    curve = builder.PiecewiseCubicZeroCurve(asOfDate, basis, curveId)
    for node in curve.nodes():
        print(node)
    plot(curve)


def testPiecewiseCubicZeroCurve2(asOfDate, basis, curveId):
    curve = builder.PiecewiseCubicZeroCurve(asOfDate, basis, curveId)
    for node in curve.nodes():
        print(node)
    maturity_dates = [ql.Date(24, 12, 2015), ql.Date(25, 2, 2016),
                      ql.Date(26, 5, 2016), ql.Date(10, 11, 2016),
                      ql.Date(30, 11, 2017), ql.Date(15, 11, 2018),
                      ql.Date(30, 11, 2020), ql.Date(30, 11, 2022),
                      ql.Date(15, 11, 2025), ql.Date(15, 11, 2045)]
    for d in maturity_dates:
        print("|%20s  %9.6f|" % (d, curve.discount(d)))

    plot(curve)


def testPiecewiseLoCubicZeroCurveDuplications():
    asOfDate = 20121211
    basis = 'Act/365F'

    curve = builder.PiecewiseCubicZeroCurve(
        asOfDate, basis, 'eonia')
    for node in curve.nodes():
        print(node)
    nodes = curve.nodes()
    temp_dates, temp_rates = zip(*nodes)
    temp_curve = ql.CubicZeroCurve(
        temp_dates, temp_rates, curve.dayCounter())

    plot(temp_curve)


def testPiecewiseLogCubicCurveDuplications():
    asOfDate = 20121211
    basis = 'Act/365F'

    curve = builder.PiecewiseLogCubicDiscountCurve(
        asOfDate, basis, 'eonia')
    for node in curve.nodes():
        print(node)
    nodes = curve.nodes()
    temp_dates, temp_rates = zip(*nodes)
    temp_curve = ql.DiscountCurve(
        temp_dates, temp_rates, curve.dayCounter())

    plot(temp_curve)


def testPiecewiseeFlatForwardCurve(asOfDate, basis, curveId):
    curve = builder.PiecewiseFlatForwardCurve(
        asOfDate, basis, curveId)
    # print(curve.dayCounter())
    today = curve.referenceDate()
    end = today + ql.Period(2, ql.Years)
    dates = [ql.Date(serial)
             for serial
             in range(today.serialNumber(), end.serialNumber() + 1)]

    rates_c = [curve.forwardRate(d,
                                 ql.TARGET().advance(d, 1, ql.Days),
                                 ql.Actual360(),
                                 ql.Simple).rate()
               for d in dates]
    pydt = [datetime.datetime(d.year(), d.month(), d.dayOfMonth())
            for d in dates]
    fig, ax = plt.subplots()
    fig.set_size_inches(10.5, 9.5)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda r, pos: '{:.2%}'.format(r)))
    plt.subplots_adjust(bottom=0.2)
    l, = plt.plot(pydt, rates_c)
    plt.show()

# https://quant.stackexchange.com/questions/44712/quantlib-python-use-zero-rates-to-get-the-originally-bootstrapped-curve


def testPiecewiseLinearZeroCurve(asOfDate, basis, curveId):
    crv = builder.PiecewiseLinearZeroCurve(
        asOfDate, basis, curveId)
    print(crv.dayCounter())
    for node in crv.nodes():
        print(node)
    dates, rates = zip(*crv.nodes())
    crv2 = ql.ZeroCurve(dates, rates, ql.Actual360())
    spot = crv.referenceDate()
    sample_dates = [spot + ql.Period(i, ql.Weeks) for i in range(15 * 52)]
    z1 = [crv.zeroRate(d, ql.Actual360(), ql.Continuous).rate()
          for d in sample_dates]
    z2 = [crv2.zeroRate(d, ql.Actual360(), ql.Continuous).rate()
          for d in sample_dates]

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date([d.to_date() for d in sample_dates], z1, '.')
    ax.plot_date([d.to_date() for d in sample_dates], z2, '-')

    plt.show()


def testOrStmt():
    basis = 'Act/360'
    # basis = ql.Actual360()
    day_count = None
    print(day_count, type(day_count))
    day_count = basis if isinstance(basis, ql.DayCounter) else ql.Actual360()
    print(day_count, type(day_count))
    print(isinstance(day_count, ql.DayCounter))


if __name__ == '__main__':
    # testPiecewiseCubicZeroCurve()
    # testPiecewiseLoCubicZeroCurveDuplications()
    # testPiecewiseLogCubicCurveDuplications()

    # testPiecewiseCubicZeroCurve(
    #     asOfDate=20121211,
    #     basis='Act/365F',
    #     curveId='eonia'
    # )

    # print(config.getCurveDir())
    # print(dfs.isExcelSerial(25570))
    # print(dfs.isYYYYMMDD(20190231))
    # testPiecewiseLogCubicCurveX(
    #     asOfDate=20121211,
    #     basis='Act/365F',
    #     curveId='eonia'
    # )

    # testPiecewiseeFlatForwardCurve(
    #     20121211, 'Act/365F', 'eonia')

    # testPiecewiseeFlatForwardCurve(
    #     20011106, 'Act/360', 'future_swap')

    # testPiecewiseLinearZeroCurve(
    #     20011106, 'Act/360', 'swap00'
    # )

    # testPiecewiseLinearZeroCurve(
    #     20011106, 'Act/360', 'fra_swap')

    # testPiecewiseLinearZeroCurve(
    #     20011106, 'Act/360', 'future_swap')

    testPiecewiseCubicZeroCurve2(
        20151130, 'Act/Act', 'bond')
