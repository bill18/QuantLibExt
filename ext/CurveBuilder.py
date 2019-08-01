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

from functools import wraps  # This convenience func preserves name and docstring
import QuantLib as ql
from . import QuantLibUtils as qlu
from . import DatetimeUtils as dfs
from . import CalendarManager as mgr
from . import Utils as utils
from . import QuantLibClassExt as qlx

# decorator to add methods to a class on the fly


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally
    return decorator

# DepositRateHelper


"""
DepositRateHelper   (
    Rate    rate,
    const boost::shared_ptr< IborIndex > &  iborIndex
)


DepositRateHelper   (
    Rate    rate,
    const Period &  tenor,
    Natural     fixingDays,
    const Calendar &    calendar,
    BusinessDayConvention   convention,
    bool    endOfMonth,
    const DayCounter &  dayCounter
)

"""


def parseDeposits(data):
    if data is None:
        return None

    helpers = []

    if not isinstance(data, list):
        data = [data]

    for rec in data:
        if 'index' in rec:  # form 2
            temp = [ql.DepositRateHelper(rate,
                                         qlu.getMarketIndex(
                                             rec['index'] + ',' + tenor)
                                         )
                    for tenor, rate in rec['marks']
                    ]
            helpers.extend(temp)
        elif 'tenor' in rec:
            tenor = dfs.parseTenor(rec['tenor'])
            calendar = mgr.getCalendar(rec['calendar'])
            rolling = qlu.getRollingConv(rec['rolling'])
            eom = rec['month_end']
            dayCount = qlu.getDayCountBasis(rec['basis'])
            # uncessary to use Quote: ql.QuoteHandle(ql.SimpleQuote(r))
            for mark in rec['marks']:
                fixingDays = mark[0]
                r = mark[1]
                temp = ql.DepositRateHelper(r,
                                            tenor,
                                            fixingDays,
                                            calendar,
                                            rolling,
                                            eom,
                                            dayCount)
                helpers.append(temp)
        elif 'settlementDays' in rec:  # form 1
            calendar = mgr.getCalendar(rec['calendar'])
            rolling = qlu.getRollingConv(rec['rolling'])
            eom = rec['month_end']
            dayCount = qlu.getDayCountBasis(rec['basis'])
            # uncessary to use Quote: ql.QuoteHandle(ql.SimpleQuote(r))
            for mark in rec['marks']:
                fixingDays = mark[0]
                r = mark[1]
                fixingDays = dfs.parseTenor(fixingDays)
                settlementDays = rec['settlementDays']
                temp = ql.DepositRateHelper(
                    r,
                    fixingDays,
                    settlementDays,
                    calendar,
                    ql.ModifiedFollowing,
                    eom,
                    dayCount
                )

                helpers.append(temp)

    return helpers


"""



FraRateHelper   (
    Rate    rate,
    Natural     monthsToStart,
    const boost::shared_ptr< IborIndex > &  iborIndex,
    Pillar::Choice  pillar = Pillar::LastRelevantDate,
    Date    customPillarDate = Date()
)

FraRateHelper   (
    Rate    rate,
    Period  periodToStart,
    const boost::shared_ptr< IborIndex > &  iborIndex,
    Pillar::Choice  pillar = Pillar::LastRelevantDate,
    Date    customPillarDate = Date()
)

FraRateHelper   (
    Rate    rate,
    Natural     monthsToStart,
    Natural     monthsToEnd,
    Natural     fixingDays,
    const Calendar &    calendar,
    BusinessDayConvention   convention,
    bool    endOfMonth,
    const DayCounter &  dayCounter,
    Pillar::Choice  pillar = Pillar::LastRelevantDate,
    Date    customPillarDate = Date()
)

FraRateHelper   (
    Rate    rate,
    Period  periodToStart,
    Natural     lengthInMonths,
    Natural     fixingDays,
    const Calendar &    calendar,
    BusinessDayConvention   convention,
    bool    endOfMonth,
    const DayCounter &  dayCounter,
    Pillar::Choice  pillar = Pillar::LastRelevantDate,
    Date    customPillarDate = Date()
)

"""


def parseFRAs(data):
    if data is None:
        return None

    helpers = []

    if not isinstance(data, list):
        data = [data]

    for rec in data:
        if 'index' in rec:
            index = qlu.getMarketIndex(rec['index'])
            for mark in rec['marks']:
                monthsToStart = mark[0]
                rate = mark[1]
                if isinstance(monthsToStart, str):
                    monthsToStart = dfs.parseTenor(monthsToStart)

                temp = ql.FraRateHelper(rate, monthsToStart, index)
                helpers.append(temp)
        else:
            fixingDays = int(rec['fixingDays'])
            calendar = mgr.getCalendar(rec['calendar'])
            rolling = qlu.getRollingConv(rec['rolling'])
            eom = rec['month_end']
            dayCount = qlu.getDayCountBasis(rec['basis'])
            for mark in rec['marks']:
                monthsToStart = mark[0]
                monthsToEnd = mark[1]
                r = mark[2]

                helper = ql.FraRateHelper(r,
                                          monthsToStart,
                                          monthsToEnd,
                                          fixingDays,
                                          calendar,
                                          rolling,
                                          eom,
                                          dayCount
                                          )
                helpers.append(helper)

        return helpers


"""
FuturesRateHelper   (
    Real    price,
    const Date &    iborStartDate,
    Natural     lengthInMonths,
    const Calendar &    calendar,
    BusinessDayConvention   convention,
    bool    endOfMonth,
    const DayCounter &  dayCounter,
    Rate    convexityAdjustment = 0.0,
    Futures::Type   type = Futures::IMM
)


FuturesRateHelper   (
    Real &     price,
    const Date &    iborStartDate,
    const Date &    iborEndDate,
    const DayCounter &  dayCounter,
    const Handle< Quote > & convexityAdjustment = Handle<Quote>(),
    Futures::Type   type = Futures::IMM
)


FuturesRateHelper   (
    Real    price,
    const Date & iborStartDate,
    const boost::shared_ptr< IborIndex > & iborIndex,
    Rate    convexityAdjustment = 0.0,
    Futures::Type   type = Futures::IMM
)
"""


def parseFutures(data):
    if data is None:
        return None

    helpers = []

    if not isinstance(data, list):
        data = [data]

    for rec in data:
        if 'index' in rec:
            iborIndex = qlu.getMarketIndex(rec['index'])
            temp = [ql.FuturesRateHelper(rate, dfs.toQLDate(iborStartDate), iborIndex)
                    for iborStartDate, rate in rec['marks']]
            helpers.extend(temp)
        elif 'months' in rec:
            months = int(rec['months'])
            calendar = mgr.getCalendar(rec['calendar'])
            rolling = qlu.getRollingConv(rec['rolling'])
            eom = rec['month_end']
            dayCount = qlu.getDayCountBasis(rec['basis'])
            for mark in rec['marks']:
                iborStartDate = mark[0]
                r = mark[1]
                convexityAdjustment = 0.0
                if len(mark) > 2:
                    convexityAdjustment = mark[2]

                helper = ql.FuturesRateHelper(r,
                                              dfs.toQLDate(iborStartDate),
                                              months,
                                              calendar,
                                              rolling,
                                              eom,
                                              dayCount,
                                              convexityAdjustment)
                helpers.append(helper)
        else:
            dayCount = qlu.getDayCountBasis(rec['basis'])
            for mark in rec['marks']:
                iborStartDate = mark[0]
                iborEndDate = mark[1]
                r = mark[2]
                convexityAdjustment = 0.0
                if len(mark) > 3:
                    convexityAdjustment = mark[3]

                helper = ql.FuturesRateHelper(r,
                                              dfs.toQLDate(iborStartDate),
                                              dfs.toQLDate(iborEndDate),
                                              dayCount,
                                              ql.QuoteHandle(ql.SimpleQuote(convexityAdjustment)))
                helpers.append(helper)

        return helpers


"""

SwapRateHelper  (
    const Handle< Quote > &     rate,
    const boost::shared_ptr< SwapIndex > &  swapIndex,
    const Handle< Quote > &     spread = Handle< Quote >(),
    const Period &  fwdStart = 0 *Days,
    const Handle< YieldTermStructure > &    discountingCurve = Handle< YieldTermStructure >(),
    Pillar::Choice  pillar = Pillar::LastRelevantDate,
    Date customPillarDate = Date()
)

SwapRateHelper  (
    const Handle< Quote > &     rate,
    const Period &  tenor,
    const Calendar &    calendar,
    Frequency   fixedFrequency,
    BusinessDayConvention   fixedConvention,
    const DayCounter &  fixedDayCount,
    const boost::shared_ptr< IborIndex > &  iborIndex,
    const Handle< Quote > &     spread = Handle< Quote >(),
    const Period &  fwdStart = 0 *Days,
    const Handle< YieldTermStructure > &    discountingCurve = Handle< YieldTermStructure >(),
    Natural     settlementDays = Null< Natural >(),
    Pillar::Choice  pillar = Pillar::LastRelevantDate,
    Date customPillarDate = Date()
)

"""


def parseSwaps(data):
    if data is None:
        return None

    helpers = []

    if not isinstance(data, list):
        data = [data]

    for rec in data:
        if 'iborIndex' in rec:
            floatIndex = qlu.getMarketIndex(rec['iborIndex'])
            fixedCalendar = mgr.getCalendar(rec["fixedLegCalendar"])

            fixedLegFrequency = qlu.getFrequency(rec["fixedLegFrequency"])
            fixedLegAdjustment = qlu.getRollingConv(rec["fixedLegAdjustment"])
            fixedLegDayCounter = qlu.getDayCountBasis(rec["fixedLegBasis"])

            for mark in rec['marks']:
                periodLength = dfs.parseTenor(mark[0])
                rate = mark[1]

                temp = ql.SwapRateHelper(
                    ql.QuoteHandle(ql.SimpleQuote(rate)),
                    periodLength,
                    fixedCalendar,
                    fixedLegFrequency,
                    fixedLegAdjustment,
                    fixedLegDayCounter,
                    floatIndex  # ql.Euribor6M()
                )

                helpers.append(temp)
        elif 'swapIndex' in rec:
            raise RuntimeError(
                "SwapRateHelper with swapIndex has not been implemented yet")
        else:
            print("iborIndex was not found")

        return helpers


"""

OISRateHelper   (
    Natural     settlementDays,
    const Period &  tenor,
    const Handle< Quote > &     fixedRate,
    const boost::shared_ptr< OvernightIndex > &     overnightIndex,
    const Handle< YieldTermStructure > &    discountingCurve = Handle<YieldTermStructure>(),
    bool    telescopicValueDates = false,
    Natural     paymentLag = 0,
    BusinessDayConvention   paymentConvention = Following,
    Frequency   paymentFrequency = Annual,
    const Calendar &    paymentCalendar = Calendar(),
    const Period &  forwardStart = 0 * Days,
    const Spread    overnightSpread = 0.0
)

DatedOISRateHelper  (
    const Date &    startDate,
    const Date &    endDate,
    const Handle< Quote > &     fixedRate,
    const boost::shared_ptr< OvernightIndex > &     overnightIndex,
    const Handle< YieldTermStructure > &    discountingCurve = Handle<YieldTermStructure>(),
    bool    telescopicValueDates = false
)

"""


def parseOISs(data):
    if data is None:
        return None

    helpers = []

    if not isinstance(data, list):
        data = [data]

    for rec in data:
        if 'settlementDays' in rec:  # form 2
            settlementDays = rec['settlementDays']
            index = qlu.getMarketIndex(rec['index'])
            temp = [ql.OISRateHelper(settlementDays, dfs.parseTenor(tenor), ql.QuoteHandle(ql.SimpleQuote(rate)), index) for
                    tenor, rate in rec['marks']]
            helpers.extend(temp)
        else:
            index = qlu.getMarketIndex(rec['index'])

            temp = [ql.DatedOISRateHelper(dfs.toQLDate(start_date),
                                          dfs.toQLDate(end_date),
                                          ql.QuoteHandle(ql.SimpleQuote(rate)),
                                          index)
                    for start_date, end_date, rate in rec['marks']]
            helpers.extend(temp)

    return helpers


"""

FixedRateBondHelper (
    const Handle< Quote > &     price,
    Natural     settlementDays,
    Real    faceAmount,
    const Schedule &    schedule,
    const std::vector< Rate > &     coupons,
    const DayCounter &  dayCounter,
    BusinessDayConvention   paymentConv = Following,
    Real    redemption = 100.0,
    const Date &    issueDate = Date(),
    const Calendar &    paymentCalendar = Calendar(),
    const Period &  exCouponPeriod = Period(),
    const Calendar &    exCouponCalendar = Calendar(),
    const BusinessDayConvention     exCouponConvention = Unadjusted,
    bool    exCouponEndOfMonth = false,
    const bool  useCleanPrice = true
)
"""


def parseBonds(data, calc_date=None, rule=None):
    if calc_date is None:
        calc_date = ql.Date.todaysDate()
    else:
        calc_date = dfs.toQLDate(calc_date)

    if rule is None:
        rule = 'Backward'

    if not isinstance(data, list):
        data = [data]
    bond_helpers = []

    rule = qlu.getDateGenRule(rule)
    for instList in data:
        day_count = qlu.getDayCountBasis(instList['basis'])
        calendar = mgr.getCalendar(instList["calendar"])
        rolling = qlu.getRollingConv(instList['rolling'])
        frequency = ql.Period(qlu.getFrequency(instList["frequency"]))
        settlement_days = instList['settlement_days']
        face_amount = instList['face_amount']
        eom = instList['month_end']

        for issue_date, maturity_date, coupon, price in instList['marks']:
            issue_date = dfs.toQLDate(issue_date)
            maturity_date = dfs.toQLDate(maturity_date)
            schedule = ql.Schedule(calc_date,
                                   maturity_date,
                                   frequency,
                                   calendar,
                                   rolling,
                                   rolling,
                                   rule,
                                   eom)

            helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(price)),
                                            settlement_days,
                                            face_amount,
                                            schedule,
                                            [coupon],
                                            day_count,
                                            rolling
                                            )
            bond_helpers.append(helper)

    return bond_helpers


def parseAll(insts, calc_date=None):
    helpers = []
    for instType in insts.keys():
        if instType == 'Deposits':
            helpers.extend(parseDeposits(insts[instType]))
        elif instType == 'OISs':
            helpers.extend(parseOISs(insts[instType]))
        elif instType == 'FRAs':
            helpers.extend(parseFRAs(insts[instType]))
        elif instType == 'Futures':
            helpers.extend(parseFutures(insts[instType]))
        elif instType == 'Swaps':
            helpers.extend(parseSwaps(insts[instType]))
        elif instType == 'Bonds':
            helpers.extend(parseBonds(insts[instType], calc_date))

    return helpers


"""
curveEngine:
    # PiecewiseConstantParameter
    PiecewiseCubicZero
    PiecewiseFlatForward
    PiecewiseFlatHazardRate
    PiecewiseLinearForward
    PiecewiseLinearZero
    PiecewiseLogCubicDiscount
    PiecewiseLogLinearDiscount
    # PiecewiseTimeDependentHestonModel
    PiecewiseYoYInflation
    PiecewiseZeroInflation
"""


def buildCurve(curveEngine, asOfDate, basis, insts, calendar=None, enableExtrapolation=True):
    engineRef = getattr(ql, curveEngine)
    if engineRef is None:
        raise RuntimeError("Curve engine %s was not found!" % curveEngine)

    evalDate = dfs.toQLDate(asOfDate)
    dayCountBasis = qlu.getDayCountBasis(basis)
    ql.Settings.instance().evaluationDate = evalDate
    helpers = parseAll(insts, asOfDate)
    jump_values = None
    jump_dates = None
    if 'Turns' in insts:
        jump_dates = [dfs.toQLDate(dt) for dt in insts["Turns"]['days']]
        jump_values = [ql.QuoteHandle(ql.SimpleQuote(v))
                       for v in insts["Turns"]['values']]

    if calendar is None:
        if jump_dates is None or jump_values is None:
            curve = engineRef(evalDate,
                              helpers,
                              dayCountBasis
                              )
        else:
            curve = engineRef(evalDate,
                              helpers,
                              dayCountBasis,
                              jump_values,
                              jump_dates)
    else:
        cal = mgr.getCalendar(calendar)
        if jump_dates is None or jump_values is None:
            curve = engineRef(0,
                              cal,
                              helpers,
                              dayCountBasis)
        else:
            curve = engineRef(0,
                              cal,
                              helpers,
                              dayCountBasis,
                              jump_values,
                              jump_dates)
    if enableExtrapolation:
        curve.enableExtrapolation()

    if curve is not None:
        return qlx.TermStructDecorator(curve)
    else:
        return None


def buildCurveWithJson(curveEngine, asOfDate, basis, instFileUrl, calendar=None, enableExtrapolation=True):
    if not (instFileUrl.startswith('file:') or instFileUrl.startswith('http:') or instFileUrl.startswith('https:')):
        instFileUrl = 'file:///' + instFileUrl

    insts = utils.loadJsonFromUrl(instFileUrl)
    return buildCurve(curveEngine, asOfDate, basis, insts, calendar, enableExtrapolation)
