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
from . import QuantLibUtils as qlu
from . import DatetimeUtils as dfs
from . import CalendarManager as mgr
from . import Utils as utils
# from . import QuantLibClassExt as qlx

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
        # print(rec)

        if 'index' in rec:  # form 2
            # iborIndexRef = qlu.getMarketIndex(rec['index'])
            temp = [ql.DepositRateHelper(rate,
                                         qlu.getMarketIndex(
                                             rec['index'] + ',' + tenor)
                                         )
                    for tenor, rate in rec['marks']
                    ]
            helpers.extend(temp)
        elif 'tenor' in rec:
            tenor = dfs.parseTenor(rec['tenor'])
            # print('---------------------------------')
            # print(tenor)
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
            # tenor = dfs.parseTenor(rec['tenor'])
            # print('---------------------------------')
            # print(tenor)
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
            # idx, tenor = rec['index'].split(',')
            iborIndex = qlu.getMarketIndex(rec['index'])
            # iborIndex = iborIndexRef(dfs.parseTenor(tenor))
            temp = [ql.FuturesRateHelper(rate, dfs.toQLDate(iborStartDate), iborIndex)
                    for iborStartDate, rate in rec['marks']]
            helpers.extend(temp)
        elif 'months' in rec:
            # tenor = dfs.parseTenor(rec['tenor'])
            # print('---------------------------------')
            # print(tenor)
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
        # idx, tenor = rec['index'].split(',')
        if 'iborIndex' in rec:
            floatIndex = qlu.getMarketIndex(rec['iborIndex'])
            fixedCalendar = mgr.getCalendar(rec["fixedLegCalendar"])
            # print(rec["fixedLegCalendar"], type(fixedCalendar))

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
        # print(rec)

        if 'settlementDays' in rec:  # form 2
            settlementDays = rec['settlementDays']
            index = qlu.getMarketIndex(rec['index'])
            # index = iborIndexRef()

            temp = [ql.OISRateHelper(settlementDays, dfs.parseTenor(tenor), ql.QuoteHandle(ql.SimpleQuote(rate)), index) for
                    tenor, rate in rec['marks']]
            helpers.extend(temp)
        else:
            # print('---------------------------------')
            index = qlu.getMarketIndex(rec['index'])
            # index = iborIndexRef()

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

    # print(type(calc_date), calc_date)

    rule = qlu.getDateGenRule(rule)
    for instList in data:
        # calc_date = dfs.toQLDate(instList['calc_date'])
        day_count = qlu.getDayCountBasis(instList['basis'])
        calendar = mgr.getCalendar(instList["calendar"])
        rolling = qlu.getRollingConv(instList['rolling'])
        frequency = ql.Period(qlu.getFrequency(instList["frequency"]))
        settlement_days = instList['settlement_days']
        face_amount = instList['face_amount']
        # coupon = instList['coupon']
        eom = instList['month_end']
        # frequency = ql.Period(6, ql.Months)

        # print(type(calc_date), calc_date)
        for issue_date, maturity_date, coupon, price in instList['marks']:
            issue_date = dfs.toQLDate(issue_date)
            maturity_date = dfs.toQLDate(maturity_date)
            # print(type(maturity_date), maturity_date)
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
            # print(helper)
            bond_helpers.append(helper)
            # termination_date = calc_date + dfs.parseTenor(m)
            # schedule = qlx.XSchedule(
            #     calc_date,
            #     termination_date,
            #     frequency,
            #     calendar,
            #     rolling,
            #     rolling,
            #     rule,
            #     eom)

            # helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(price)),
            #                                 settlement_days,
            #                                 face_amount,
            #                                 schedule,
            #                                 [coupon],
            #                                 day_count,
            #                                 rolling
            #                                 )
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


# Dynamic version of Decorator Pattern: intercept live attributes

class YieldTermStructureDecorator(object):
    def __init__(self, termStructrure, calendar):
        self._term_struct = termStructrure
        self._calendar = calendar

    def __getattr__(self, name):
        return getattr(self._term_struct, name)

    # =======================================================
    # DiscountFactor discount(const Date&,
    #      bool extrapolate = false);
    # -------------------------------------------------------
    # DiscountFactor discount(Time,
    #      bool extrapolate = false);
    # =======================================================
    def discount(self, *args):
        if isinstance(args[0], ql.Date) or dfs.isYYYYMMDD(args[0]):
            newArgs = [
                dfs.toQLDate(args[0])
            ]
        else:
            newArgs = [
                args[0]
            ]

        if len(args) > 1:
            newArgs.append(args[1])

        return self._term_struct.discount(*tuple(newArgs))

    # =======================================================
    # InterestRate zeroRate(const Date& d,
    #      const DayCounter&,
    #      Compounding,
    #      Frequency f = Annual,
    #      bool extrapolate = false) const;
    # -------------------------------------------------------
    # InterestRate zeroRate(Time t,
    #      Compounding,
    #      Frequency f = Annual,
    #      bool extrapolate = false) const;
    # =======================================================
    def zeroRate(self, *args):
        if isinstance(args[1], ql.DayCounter) or isinstance(args[1], str):
            newArgs = [
                dfs.toQLDate(args[0]),
                qlu.getDayCountBasis(args[1]),
                qlu.getCompoundType(args[2])
            ]

            if len(args) > 3:
                newArgs.append(qlu.getFrequency(args[3]))
            if len(args) > 4:
                newArgs.append(args[4])
        else:
            newArgs = [
                args[0],
                qlu.getCompoundType(args[1])
            ]

            if len(args) > 2:
                newArgs.append(qlu.getFrequency(args[2]))
            if len(args) > 3:
                newArgs.append(args[3])

        return self._term_struct.zeroRate(*tuple(newArgs))

    # =======================================================
    # InterestRate forwardRate(const Date& d1,
    #      const Date& d2,
    #      const DayCounter&,
    #      Compounding,
    #      Frequency f = Annual,
    #      bool extrapolate = false) const;
    # -------------------------------------------------------
    # InterestRate forwardRate(Time t1,
    #      Time t2,
    #      Compounding,
    #      Frequency f = Annual,
    #      bool extrapolate = false) const;
    # =======================================================
    def forwardRate(self, *args):
        if isinstance(args[2], ql.DayCounter) or isinstance(args[2], str):
            newArgs = [
                dfs.toQLDate(args[0]),
                dfs.toQLDate(args[1]),
                qlu.getDayCountBasis(args[2]),
                qlu.getCompoundType(args[3])
            ]

            if len(args) > 4:
                newArgs.append(qlu.getFrequency(args[4]))
            if len(args) > 5:
                newArgs.append(args[5])
        else:
            newArgs = [
                args[0],
                args[1],
                qlu.getCompoundType(args[2])
            ]

            if len(args) > 3:
                newArgs.append(qlu.getFrequency(args[3]))
            if len(args) > 4:
                newArgs.append(args[4])

        return self._term_struct.forwardRate(*tuple(newArgs))

    # def zeroRate(self, endDate, compounding=ql.Compounded, freq=ql.Annual):
    #     endDate = endDate if isinstance(
    #         endDate, ql.Date) else dfs.toQLDate(endDate)
    #     compounding = compounding if isinstance(
    #         compounding, int) else qlu.getCompoundType(compounding)
    #     startDate = self._term_struct.referenceDate()
    #     dc = self._term_struct.dayCounter()
    #     years = dc.yearFraction(startDate, endDate)
    #     freq = freq if isinstance(
    #         freq, int) else qlu.getFrequency(freq)
    #     return self._term_struct.zeroRate(years, compounding, freq)

    # def discount(self, endDate, extrapolate=False):
    #     endDate = endDate if isinstance(
    #         endDate, ql.Date) else dfs.toQLDate(endDate)
    #     return self._term_struct.discount(endDate, extrapolate)

    # def forwardRate(self, startDate, endDate, dayCount=None, compounding=ql.Compounded, freq=ql.Annual):
    #     if dayCount is None:
    #         dayCount = self._term_struct.dayCounter()
    #     else:
    #         dayCount = dayCount if isinstance(
    #             dayCount, ql.DayCounter) else qlu.getDayCountBasis(dayCount)
    #     startDate = startDate if isinstance(
    #         startDate, ql.Date) else dfs.toQLDate(startDate)
    #     endDate = endDate if isinstance(
    #         endDate, ql.Date) else dfs.toQLDate(endDate)
    #     compounding = compounding if isinstance(
    #         compounding, int) else qlu.getCompoundType(compounding)
    #     freq = freq if isinstance(
    #         freq, int) else qlu.getFrequency(freq)
    #     return self._term_struct.forwardRate(startDate, endDate, dayCount, compounding, freq)

    def oneDayForwardRates(self, period, calendar, startDate=None, dayCount=None, compounding=ql.Compounded, freq=ql.Annual):
        startDate = startDate if startDate is not None else self._term_struct.referenceDate()
        startDate = startDate if isinstance(
            startDate, ql.Date) else dfs.toQLDate(startDate)
        period = period if isinstance(
            period, ql.Period) else qlu.parseTenor(period)
        endDate = startDate + period
        if dayCount is None:
            dayCount = self._term_struct.dayCounter()
        else:
            dayCount = dayCount if isinstance(
                dayCount, ql.DayCounter) else qlu.getDayCountBasis(dayCount)
        dates = [ql.Date(serial)
                 for serial
                 in range(startDate.serialNumber(), endDate.serialNumber() + 1)]

        if calendar is None and self._calendar is None:
            raise RuntimeError('You must provide a calendar')

        if calendar is None:
            calendar = self._term_struct.calendar()
        else:
            calendar = calendar if isinstance(
                calendar, ql.Calendar) else mgr.getCalendar(calendar)

        # print('... in oneDayForwardRates ...', calendar, type(calendar), ' ...')
        rates = [self.forwardRate(d,
                                  calendar.advance(d, 1, ql.Days), dayCount, compounding, freq).rate()
                 for d in dates]
        # print(rates)
        return {'dates': dates, 'rates': rates}

    # Two methods we don't actually want to intercept,
    # but iter() and next() will be upset without them.

    # def __iter__(self):
    #     return self._term_struct.__iter__()

    # def __next__(self):
    #     return self._term_struct.__next__()

    # Offer every other method and property dynamically.

    # def __getattr__(self, name):
    #     return getattr(self._term_struct, name)

    # def __setattr__(self, name, value):
    #     setattr(self._term_struct, name, value)

    # def __delattr__(self, name):
    #     delattr(self._term_struct, name)


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
        # print(jump_dates)
        # print(jump_values)
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
        return YieldTermStructureDecorator(curve, calendar)
    else:
        return None

# instFileUrl can be either file or http URL


def buildCurveWithJson(curveEngine, asOfDate, basis, instFileUrl, calendar=None, enableExtrapolation=True):
    if not (instFileUrl.startswith('file:') or instFileUrl.startswith('http:') or instFileUrl.startswith('https:')):
        instFileUrl = 'file:///' + instFileUrl

    insts = utils.loadJsonFromUrl(instFileUrl)
    return buildCurve(curveEngine, asOfDate, basis, insts, calendar, enableExtrapolation)
