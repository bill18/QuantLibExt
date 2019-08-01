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
from . import CalendarManager as clm
from . import ScheduleManager as scm

# https://rkapl123.github.io/QLAnnotatedSource/modules.html
# ===================================================================================
# Money   ()
# -----------------------------------------------------------------------------------
# Money   (const Currency &    currency,
#          Decimal     value )
# -----------------------------------------------------------------------------------
# Money   (Decimal     value,
#         const Currency &    currency)
# ===================================================================================


class Money(ql.Money):
    def __init__(self, *args):
        newArgs = ()
        if len(args) == 2:
            if isinstance(args[0], ql.Currency) or isinstance(args[0], str):
                newArgs = (
                    qlu.getCurrency(args[0]),
                    args[1]
                )
            else:
                newArgs = (
                    args[0],
                    qlu.getCurrency(args[1])
                )

        super().__init__(*newArgs)


# ===================================================================================
# InterestRate (
#         Rate              r,
#         const DayCounter &dc,
#         Compounding  comp,
#         Frequency    freq
#     )
# ===================================================================================

class InterestRate(ql.InterestRate):
    def __init__(self, rate, basis, compound, frequency):
        dayCount = qlu.getDayCountBasis(basis)
        compoundType = qlu.getCompoundType(compound)
        freq = qlu.getFrequency(frequency)
        super().__init__(rate, dayCount, compoundType, freq)

    def discountFactor(self, d1, d2, *vargs):
        newArgs = [
            dfs.toQLDate(d1),
            dfs.toQLDate(d2)
        ]
        if len(vargs) > 0:
            newArgs.append(dfs.toQLDate(vargs[0]))
        if len(vargs) > 1:
            newArgs.append(dfs.toQLDate(vargs[1]))

        return super().discountFactor(*tuple(newArgs))

    # ------------------------------------------------------
    # Real compoundFactor(Time    t   )   const
    # Real compoundFactor(const Date &    d1,
    #         const Date &    d2,
    #         const Date &    refStart = Date(),
    #         const Date &    refEnd = Date()
    # )       const
    # ------------------------------------------------------

    def compoundFactor(self, *args):
        if len(args) == 1:
            newArgs = [args[0]]
        elif len(args) >= 2:
            newArgs = [
                dfs.toQLDate(args[0]),
                dfs.toQLDate(args[1])
            ]
        if len(args) > 0:
            newArgs.append(dfs.toQLDate(args[0]))
        if len(args) > 1:
            newArgs.append(dfs.toQLDate(args[1]))
        return super().compoundFactor(*tuple(newArgs))

    def equivalentRate(self, compound, frequency, years):
        compoundType = qlu.getCompoundType(compound)
        freq = qlu.getFrequency(frequency)
        return super().equivalentRate(compoundType, freq, years)

# ====================================================================================
# Schedule    (
#     const std::vector< Date > &     dates,
#     const Calendar &    calendar = NullCalendar(),
#     const BusinessDayConvention     convention = Unadjusted,
#     boost::optional< BusinessDayConvention >    terminationDateConvention = boost::none,
#     const boost::optional< Period >     tenor = boost::none,
#     boost::optional< DateGeneration::Rule >     rule = boost::none,
#     boost::optional< bool >     endOfMonth = boost::none,
#     const std::vector< bool > &     isRegular = std::vector<bool>(0)
# )
# ------------------------------------------------------------------------------------
# Schedule    (
#     Date    effectiveDate,
#     const Date &    terminationDate,
#     const Period &  tenor,
#     const Calendar &    calendar,
#     BusinessDayConvention   convention,
#     BusinessDayConvention   terminationDateConvention,
#     DateGeneration::Rule    rule,
#     bool    endOfMonth,
#     const Date &    firstDate = Date(),
#     const Date &    nextToLastDate = Date()
# )
# ====================================================================================


class Schedule(ql.Schedule):
    def __init__(self, *args):
        if len(args) >= 3:
            if isinstance(args[0], ql.Date) or isinstance(args[0], int):
                newArgs = [
                    dfs.toQLDate(args[0]),
                    dfs.toQLDate(args[1]),
                    qlu.parseTenor(args[2]),
                    clm.getCalendar(args[3]),
                    qlu.getRollingConv(args[4]),
                    qlu.getRollingConv(args[5]),
                    dfs.toQLDate(args[6]),
                    args[7],
                ]

                if len(args) > 8:
                    newArgs.append(dfs.toQLDate(args[8]))
                if len(args) > 9:
                    newArgs.append(dfs.toQLDate(args[9]))
            elif isinstance(args[0], list) or isinstance(args[0], tuple):
                newArgs = [
                    [dfs.toQLDate(dt) for dt in args[0]]
                ]

                if len(args) > 1:
                    newArgs.append(clm.getCalendar(args[1]))
                if len(args) > 2:
                    newArgs.append(qlu.getRollingConv(args[2]))
                if len(args) > 3:
                    newArgs.append(qlu.getRollingConv(args[3]))
                if len(args) > 4:
                    newArgs.append(qlu.parseTenor(args[4]))
                if len(args) > 5:
                    newArgs.append(qlu.getDateGenRule(args[5]))
                if len(args) > 6:
                    newArgs.append(args[6])
                if len(args) > 7:
                    newArgs.append(args[7])
            else:
                newArgs = []
            # print(tuple(newArgs))
            newArgs = tuple(newArgs)
            super().__init__(*newArgs)
        else:
            raise RuntimeError('Invalid input for Schedule')


class BondDecorator(object):
    def __init__(self, bond):
        self._bond = bond

    def __getattr__(self, name):
        return getattr(self._bond, name)

    # =======================================================
    #     Real accruedAmount    (   Date    d = Date()  )
    # =======================================================
    def accruedAmount(self, *args):
        newArgs = []

        if len(args) > 0:
            newArgs.append(dfs.toQLDate(args[0]))

        return self._bond.accruedAmount(*tuple(newArgs))

    # =======================================================
    # Rate  bondYield ( DayCounter &dc,
    #      Compounding comp,
    #      Frequency freq,
    #      Real accuracy=1.0e-8,
    #      Size maxEvaluations=100)
    # -------------------------------------------------------
    # Rate  bondYield (Real cleanPrice,
    #       DayCounter &dc,
    #      Compounding comp,
    #      Frequency freq,
    #      Date settlementDate=Date(),
    #      Real accuracy=1.0e-8,
    #      Size maxEvaluations=100)
    # =======================================================
    def bondYield(self, *args):
        if isinstance(args[0], ql.DayCounter) or isinstance(args[0], str):
            newArgs = [
                qlu.getDayCountBasis(args[0]),
                qlu.getCompoundType(args[1]),
                qlu.getFrequency(args[2]),
            ]

            if len(args) > 3:
                newArgs.append(args[3])
            if len(args) > 4:
                newArgs.append(args[4])
        else:
            newArgs = [
                args[0],
                qlu.getDayCountBasis(args[1]),
                qlu.getCompoundType(args[2]),
                qlu.getFrequency(args[3]),
            ]

            if len(args) > 4:
                newArgs.append(dfs.toQLDate(args[4]))
            if len(args) > 5:
                newArgs.append(args[5])
            if len(args) > 6:
                newArgs.append(args[6])

        return self._bond.bondYield(*tuple(newArgs))

    # =======================================================
    #     Date  settlementDate (Date d=Date())
    # =======================================================
    def settlementDate(self, *args):
        newArgs = [
        ]

        if len(args) > 0:
            newArgs.append(dfs.toQLDate(args[0]))

        return self._bond.settlementDate(*tuple(newArgs))

    # =======================================================
    # Real  cleanPrice (Rate yield,
    #       DayCounter &dc,
    #      Compounding comp,
    #      Frequency freq,
    #      Date settlementDate=Date())
    # =======================================================
    def cleanPrice(self, *args):
        newArgs = [
            args[0],
            qlu.getDayCountBasis(args[1]),
            qlu.getCompoundType(args[2]),
            qlu.getFrequency(args[3]),
        ]

        if len(args) > 4:
            newArgs.append(dfs.toQLDate(args[4]))

        return self._bond.cleanPrice(*tuple(newArgs))

    # =======================================================
    # Real  dirtyPrice (Rate yield,
    #       DayCounter &dc,
    #      Compounding comp,
    #      Frequency freq,
    #      Date settlementDate=Date())
    # =======================================================
    def dirtyPrice(self, *args):
        newArgs = [
            args[0],
            qlu.getDayCountBasis(args[1]),
            qlu.getCompoundType(args[2]),
            qlu.getFrequency(args[3]),
        ]

        if len(args) > 4:
            newArgs.append(dfs.toQLDate(args[4]))

        return self._bond.dirtyPrice(*tuple(newArgs))

    # =======================================================
    #     Real  settlementValue (Real cleanPrice)
    # =======================================================
    def settlementValue(self, *args):
        newArgs = [
            args[0]
        ]

        return self._bond.settlementValue(*tuple(newArgs))

    # =======================================================
    #     Rate  nextCouponRate (Date d=Date())
    # =======================================================
    def nextCouponRate(self, *args):
        newArgs = [
        ]

        if len(args) > 0:
            newArgs.append(dfs.toQLDate(args[0]))

        return self._bond.nextCouponRate(*tuple(newArgs))

    # =======================================================
    #     Real  notional (Date d=Date())
    # =======================================================
    def notional(self, *args):
        newArgs = [
        ]

        if len(args) > 0:
            newArgs.append(dfs.toQLDate(args[0]))

        return self._bond.notional(*tuple(newArgs))

    # =======================================================
    #     Rate  previousCouponRate (Date d=Date()) const
    # =======================================================
    def previousCouponRate(self, *args):
        newArgs = [
        ]

        if len(args) > 0:
            newArgs.append(dfs.toQLDate(args[0]))

        return self._bond.previousCouponRate(*tuple(newArgs))


# ===================================================================================
#
# FixedRateBond   (
#         Natural     settlementDays,
#         Real    faceAmount,
#         const Schedule &    schedule,
#         const std::vector< Rate > &     coupons,
#         const DayCounter &      accrualDayCounter,
#         BusinessDayConvention   paymentConvention = Following,
#         Real    redemption = 100.0,
#         const Date &    issueDate = Date(),
#          const Calendar &    paymentCalendar = Calendar(),
#          const Period &      exCouponPeriod = Period(),
#          const Calendar &    exCouponCalendar = Calendar(),
#          const BusinessDayConvention     exCouponConvention = Unadjusted,
#          bool    exCouponEndOfMonth = false
#      )

# FixedRateBond   (
#         Natural     settlementDays,
#         const Calendar &    couponCalendar,
#         Real    faceAmount,
#         const Date &    startDate,
#         const Date &    maturityDate,
#         const Period &      tenor,
#         const std::vector< Rate > &     coupons,
#         const DayCounter &      accrualDayCounter,
#          BusinessDayConvention   accrualConvention = Following,
#          BusinessDayConvention   paymentConvention = Following,
#          Real    redemption = 100.0,
#          const Date &    issueDate = Date(),
#          const Date &    stubDate = Date(),
#          DateGeneration::Rule    rule = DateGeneration::Backward,
#          bool    endOfMonth = false,
#          const Calendar &    paymentCalendar = Calendar(),
#          const Period &      exCouponPeriod = Period(),
#          const Calendar &    exCouponCalendar = Calendar(),
#          const BusinessDayConvention     exCouponConvention = Unadjusted,
#          bool    exCouponEndOfMonth = false
#      )

# FixedRateBond   (
#        Natural     settlementDays,
#        Real    faceAmount,
#        const Schedule &    schedule,
#        const std::vector< InterestRate > &     coupons,
#        BusinessDayConvention   paymentConvention = Following,
#        Real    redemption = 100.0,
#        const Date &    issueDate = Date(),
#        const Calendar &    paymentCalendar = Calendar(),
#         const Period &      exCouponPeriod = Period(),
#         const Calendar &    exCouponCalendar = Calendar(),
#         const BusinessDayConvention     exCouponConvention = Unadjusted,
#         bool    exCouponEndOfMonth = false
#     )
# ===================================================================================
# if 2rd argument is Calendar then use constructor 2 (8 mandatory)
# if 6th argument is DayCounter then use constructor 1 (5 mandatory)
# otherwise constructor 3 (4 mandatory)


class XFixedRateBond(ql.FixedRateBond):
    def __init__(self, *args):
        if len(args) < 4:
            raise RuntimeError(
                'Invalid arguments, at least 4 need to be provided')
        # for i, a in enumerate(args):
        #     print("%d: %s" % (i, type(a)))

        if isinstance(args[4], ql.DayCounter) or isinstance(args[4], str):
            # print('... case 1 ...')
            # case 1
            newArgs = [
                args[0],
                args[1],
                scm.getSchedule(args[2]),
                args[3],
                qlu.getDayCountBasis(args[4])
            ]
            if len(args) > 5:
                newArgs.append(qlu.getRollingConv(args[5]))
            if len(args) > 6:
                newArgs.append(args[6])
            if len(args) > 7:
                newArgs.append(dfs.toQLDate(args[7]))
            if len(args) > 8:
                newArgs.append(clm.getCalendar(args[8]))
            if len(args) > 9:
                newArgs.append(qlu.parseTenor(args[9]))
            if len(args) > 10:
                newArgs.append(clm.getCalendar(args[10]))
            if len(args) > 11:
                newArgs.append(qlu.getRollingConv(args[11]))
            if len(args) > 12:
                newArgs.append(args[12])

        elif isinstance(args[4], int) or isinstance(args[4], str):
            # case 3
            # print('... case 3')
            newArgs = [
                args[0],
                args[1],
                scm.getSchedule(args[2]),
                args[3]
            ]

            if len(args) > 4:
                # print(args)
                newArgs.append(qlu.getRollingConv(args[4]))
            if len(args) > 5:
                newArgs.append(args[5])
            if len(args) > 6:
                newArgs.append(dfs.toQLDate(args[6]))
            if len(args) > 7:
                newArgs.append(clm.getCalendar(args[7]))
            if len(args) > 8:
                newArgs.append(qlu.parseTenor(args[8]))
            if len(args) > 9:
                newArgs.append(clm.getCalendar(args[9]))
            if len(args) > 10:
                newArgs.append(qlu.getRollingConv(args[10]))
            if len(args) > 11:
                newArgs.append(args[11])
        else:
            # case 2
            # print('... case 2')
            newArgs = [
                args[0],
                clm.getCalendar(args[1]),
                args[2],
                dfs.toQLDate(args[3]),
                dfs.toQLDate(args[4]),
                qlu.parseTenor(args[5]),
                args[6],
                qlu.getDayCountBasis(args[7])
            ]
            if len(args) > 8:
                newArgs.append(qlu.getRollingConv(args[8]))
            if len(args) > 9:
                newArgs.append(qlu.getRollingConv(args[9]))
            if len(args) > 10:
                newArgs.append(args[10])
            if len(args) > 11:
                newArgs.append(dfs.toQLDate(args[11]))
            if len(args) > 12:
                newArgs.append(dfs.toQLDate(args[12]))
            if len(args) > 13:
                newArgs.append(qlu.getDateGenRule(args[13]))
            if len(args) > 14:
                newArgs.append(args[14])
            if len(args) > 15:
                newArgs.append(clm.getCalendar(args[15]))
            if len(args) > 16:
                newArgs.append(qlu.parseTenor(args[16]))
            if len(args) > 17:
                newArgs.append(clm.getCalendar(args[17]))
            if len(args) > 18:
                newArgs.append(qlu.getRollingConv(args[18]))
            if len(args) > 19:
                newArgs.append(args[19])

        # print(newArgs)
        # super().__init__(newArgs[0], newArgs[1],
        #                  newArgs[2], newArgs[3], newArgs[4])
        super().__init__(*tuple(newArgs))


def FixedRateBond(*args, curve, engine):
    bond = XFixedRateBond(*args)
    bondEngine = qlu.getPricingEngine(engine,
                                      ql.YieldTermStructureHandle(curve))
    bond.setPricingEngine(bondEngine)
    return BondDecorator(bond)

# =============================================================================
# VanillaSwap (   Type    type,
#     Real    nominal,
#     const Schedule &    fixedSchedule,
#     Rate    fixedRate,
#     const DayCounter &  fixedDayCount,
#     const Schedule &    floatSchedule,
#     const boost::shared_ptr< IborIndex > &  iborIndex,
#     Spread  spread,
#     const DayCounter &  floatingDayCount,
#     boost::optional< BusinessDayConvention > paymentConvention = boost::none
# )
# =============================================================================


class VanillaSwap(ql.VanillaSwap):
    def __init__(self, *args):
        if len(args) < 8:
            raise RuntimeError(
                "Invalid arguments, mandatory number of arguments is 8")

        newArgs = [args[0],
                   scm.getSchedule(args[1]),
                   args[2],
                   qlu.getDayCountBasis(args[3]),
                   scm.getSchedule(args[4]),
                   qlu.getMarketIndex(args[5]),
                   args[6],
                   qlu.getDayCountBasis(args[7])
                   ]
        if len(args) > 8:
            newArgs.append(qlu.getRollingConv(args[8]))

        super().__init__(*tuple(newArgs))


# =============================================================================
# ZeroCouponBond  (
#     Natural     settlementDays,
#     const Calendar &    calendar,
#     Real    faceAmount,
#     const Date &    maturityDate,
#     BusinessDayConvention   paymentConvention = Following,
#     Real    redemption = 100.0,
#     const Date &    issueDate = Date()
# )
# =============================================================================

class XZeroCouponBond(ql.ZeroCouponBond):
    def __init__(self, *args):
        newArgs = [
            args[0],
            clm.getCalendar(args[1]),
            args[2],
            dfs.toQLDate(args[3]),
        ]

        if len(args) > 4:
            newArgs.append(qlu.getRollingConv(args[4]))
        if len(args) > 5:
            newArgs.append(args[5])
        if len(args) > 6:
            newArgs.append(dfs.toQLDate(args[6]))

        super().__init__(*tuple(newArgs))


def ZeroCouponBond(*args):
    bond = XZeroCouponBond(*args)
    return BondDecorator(bond)

# ======================================================
# Bond(
#     Natural     settlementDays,
#     const Calendar & calendar,
#     const Date & issueDate=Date(),
#     const Leg & coupons=Leg()
# )
# ------------------------------------------------------
# Bond(
#     Natural     settlementDays,
#     const Calendar & calendar,
#     Real    faceAmount,
#     const Date & maturityDate,
#     const Date & issueDate=Date(),
#     const Leg & cashflows=Leg()
# )
# ======================================================


class XBond(ql.Bond):
    """docstring for Bond"""

    def __init__(self, *args):
        if isinstance(args[2], ql.Date):
            newArgs = [
                args[0],
                clm.getCalendar(args[1])
            ]

            if len(args) > 2:
                newArgs.append(dfs.toQLDate(args[2]))
            if len(args) > 3:
                newArgs.append(args[3])
        else:
            newArgs = [
                args[0],
                clm.getCalendar(args[1]),
                args[2],
                dfs.toQLDate(args[3])
            ]

            if len(args) > 4:
                newArgs.append(dfs.toQLDate(args[4]))
            if len(args) > 5:
                newArgs.append(args[5])

        super().__init__(*tuple(newArgs))


def Bond(*args):
    bond = XBond(*args)
    return BondDecorator(bond)


class ForwardDecorator(object):
    def __init__(self, forward):
        self._forward = forward

    def __getattr__(self, name):
        return getattr(self._forward, name)

    # =======================================================
    # InterestRate  impliedYield (Real underlyingSpotValue,
    #      Real forwardValue,
    #      Date settlementDate,
    #      Compounding compoundingConvention,
    #      DayCounter dayCounter)
    # =======================================================
    def impliedYield(self, *args):
        newArgs = [
            args[0],
            args[1],
            dfs.toQLDate(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getDayCountBasis(args[4])
        ]

        return self._forward.impliedYield(*tuple(newArgs))

# ==========================================================================================
# FixedRateBondForward    (
#     const Date &    valueDate,
#     const Date &    maturityDate,
#     Position::Type  type,
#     Real    strike,
#     Natural     settlementDays,
#     const DayCounter &  dayCounter,
#     const Calendar &    calendar,
#     BusinessDayConvention   businessDayConvention,
#     const boost::shared_ptr< FixedRateBond > &  fixedCouponBond,
#     const Handle< YieldTermStructure > & discountCurve = Handle<YieldTermStructure>(),
#     const Handle< YieldTermStructure > & incomeDiscountCurve = Handle<YieldTermStructure>()
# )
# ==========================================================================================


class XFixedRateBondForward(ql.FixedRateBondForward):
    def __init__(self, *args):
        newArgs = [
            dfs.toQLDate(args[0]),
            dfs.toQLDate(args[1]),
            qlu.getPositionType(args[2]),
            args[3],
            args[4],
            qlu.getDayCountBasis(args[5]),
            clm.getCalendar(args[6]),
            qlu.getRollingConv(args[7]),
            args[8],
        ]

        if len(args) > 9:
            newArgs.append(args[9])
        if len(args) > 10:
            newArgs.append(args[10])

        # for i, a in enumerate(newArgs):
        #     print("%d:%s" % (i, type(a)))
        super().__init__(*tuple(newArgs))


def FixedRateBondForward(*args):
    fwd = XFixedRateBondForward(*args)
    return ForwardDecorator(fwd)

# InterpolatedZeroCurve(const std::vector<Date>& dates,
#                       const std::vector<Rate>& yields,
#                       const DayCounter& dayCounter,
#                       const Calendar& calendar = Calendar(),
#                       const Interpolator& i = Interpolator(),
#                       Compounding compounding = Continuous,
#                       Frequency frequency = Annual);


class XZeroCurve(ql.ZeroCurve):
    def __init__(self, *args):
        newArgs = [
            [dfs.toQLDate(dt) for dt in args[0]],
            args[1],
            qlu.getDayCountBasis(args[2]),
        ]

        if len(args) > 3:
            newArgs.append(clm.getCalendar(args[3]))
        if len(args) > 4:
            newArgs.append(qlu.getInterpolationMethod(args[4]))
        if len(args) > 5:
            newArgs.append(qlu.getCompoundType(args[5]))
        if len(args) > 6:
            newArgs.append(qlu.getFrequency(args[6]))
        super().__init__(*tuple(newArgs))


class TermStructDecorator(object):
    def __init__(self, term_struct):
        self._term_struct = term_struct

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


def ZeroCurve(*args):
    crv = XZeroCurve(*args)
    return TermStructDecorator(crv)


# InterpolatedDiscountCurve(const std::vector<Date>& dates,
#                           const std::vector<DiscountFactor>& discounts,
#                           const DayCounter& dayCounter,
#                           const Calendar& calendar = Calendar(),
#                           const Interpolator& i = Interpolator());

# DiscountFactor is of type "double" in QuantLib C++

class XDiscountCurve(ql.DiscountCurve):
    def __init__(self, *args):
        newArgs = [
            [dfs.toQLDate(dt) for dt in args[0]],
            args[1],
            qlu.getDayCountBasis(args[2]),
        ]

        if len(args) > 3:
            newArgs.append(clm.getCalendar(args[3]))
        if len(args) > 4:
            newArgs.append(args[4])

        super().__init__(*tuple(newArgs))


def DiscountCurve(*args):
    crv = XDiscountCurve(*args)
    return TermStructDecorator(crv)

#   InterpolatedForwardCurve(const std::vector<Date>& dates,
#                            const std::vector<Rate>& forwards,
#                            const DayCounter& dayCounter,
#                            const Calendar& calendar = Calendar(),
#                            const Interpolator& i = Interpolator());


class XForwardCurve(ql.ForwardCurve):
    def __init__(self, *args):
        newArgs = [
            [dfs.toQLDate(dt) for dt in args[0]],
            args[1],
            qlu.getDayCountBasis(args[2]),
        ]

        if len(args) > 3:
            newArgs.append(clm.getCalendar(args[3]))
        if len(args) > 4:
            newArgs.append(args[4])

        super().__init__(*tuple(newArgs))


def ForwardCurve(*args):
    crv = XForwardCurve(*args)
    return TermStructDecorator(crv)
