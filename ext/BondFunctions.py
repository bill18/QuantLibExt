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
from . import DatetimeUtils as dfs
from . import QuantLibUtils as qlu
from . import QuantLibClassExt as qlx

# =======================================================
#     static Date   startDate (const Bond &bond)
# =======================================================


def startDate(*args):
    newArgs = [
        args[0]
    ]

    return ql.BondFunctions.startDate(*tuple(newArgs))


# =======================================================
#     static Date   maturityDate (const Bond &bond)
# =======================================================
def maturityDate(*args):
    newArgs = [
        args[0]
    ]

    return ql.BondFunctions.maturityDate(*tuple(newArgs))


# =======================================================
# static bool   isTradable (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def isTradable(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.isTradable(*tuple(newArgs))


# =======================================================
# static Leg::const_reverse_iterator    previousCashFlow (const Bond &bond,
#      Date refDate=Date())
# =======================================================
def previousCashFlow(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.previousCashFlow(*tuple(newArgs))


# =======================================================
# static Leg::const_iterator    nextCashFlow (const Bond &bond,
#      Date refDate=Date())
# =======================================================
def nextCashFlow(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.nextCashFlow(*tuple(newArgs))


# =======================================================
# static Date   previousCashFlowDate (const Bond &bond,
#      Date refDate=Date())
# =======================================================
def previousCashFlowDate(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.previousCashFlowDate(*tuple(newArgs))


# =======================================================
# static Date   nextCashFlowDate (const Bond &bond,
#      Date refDate=Date())
# =======================================================
def nextCashFlowDate(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.nextCashFlowDate(*tuple(newArgs))


# =======================================================
# static Real   previousCashFlowAmount (const Bond &bond,
#      Date refDate=Date())
# =======================================================
def previousCashFlowAmount(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.previousCashFlowAmount(*tuple(newArgs))


# =======================================================
# static Real   nextCashFlowAmount (const Bond &bond,
#      Date refDate=Date())
# =======================================================
def nextCashFlowAmount(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.nextCashFlowAmount(*tuple(newArgs))


# =======================================================
# static Rate   previousCouponRate (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def previousCouponRate(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.previousCouponRate(*tuple(newArgs))


# =======================================================
# static Rate   nextCouponRate (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def nextCouponRate(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.nextCouponRate(*tuple(newArgs))


# =======================================================
# static Date   accrualStartDate (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def accrualStartDate(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.accrualStartDate(*tuple(newArgs))


# =======================================================
# static Date   accrualEndDate (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def accrualEndDate(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.accrualEndDate(*tuple(newArgs))


# =======================================================
# static Date   referencePeriodStart (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def referencePeriodStart(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.referencePeriodStart(*tuple(newArgs))


# =======================================================
# static Date   referencePeriodEnd (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def referencePeriodEnd(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.referencePeriodEnd(*tuple(newArgs))


# =======================================================
# static Time   accrualPeriod (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def accrualPeriod(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.accrualPeriod(*tuple(newArgs))


# =======================================================
# static Date::serial_type  accrualDays (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def accrualDays(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.accrualDays(*tuple(newArgs))


# =======================================================
# static Time   accruedPeriod (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def accruedPeriod(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.accruedPeriod(*tuple(newArgs))


# =======================================================
# static Date::serial_type  accruedDays (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def accruedDays(*args):
    newArgs = [
        args[0]
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.accruedDays(*tuple(newArgs))


# =======================================================
# static Real   accruedAmount (const Bond &bond,
#      Date settlementDate=Date())
# =======================================================
def accruedAmount(*args):
    newArgs = [
        args[0],
    ]

    if len(args) > 1:
        newArgs.append(dfs.toQLDate(args[1]))

    return ql.BondFunctions.accruedAmount(*tuple(newArgs))


# =======================================================
# static Rate   atmRate (const Bond &bond,
#      const YieldTermStructure &discountCurve,
#      Date settlementDate=Date(),
#      Real cleanPrice=Null< Real >())
# =======================================================
def atmRate(*args):
    newArgs = [
        args[0],
        args[1]
    ]

    if len(args) > 2:
        newArgs.append(dfs.toQLDate(args[2]))
    if len(args) > 3:
        newArgs.append(args[3])

    return ql.BondFunctions.atmRate(*tuple(newArgs))


# =======================================================
# static Real   cleanPrice (const Bond &bond,
#      const InterestRate &yield,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   cleanPrice (const Bond &bond,
#      const YieldTermStructure &discountCurve,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   cleanPrice (const Bond &bond,
#      Rate yield,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   cleanPrice (const Bond &bond,
#      const boost::shared_ptr<YieldTermStructure> &discount,
#      Spread zSpread,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date())
# =======================================================


def cleanPrice(*args):
    # case 2
    if isinstance(args[1], ql.YieldTermStructure) and len(args) <= 3:
        newArgs = [
            args[0],
            args[1]
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    # case 1
    elif isinstance(args[1], ql.InterestRate):
        newArgs = [
            args[0],
            args[1]
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    # case 3
    elif isinstance(args[2], ql.DayCounter) or isinstance(args[2], str):
        # def cleanPrice(*args):
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4]),
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))
    else:
        newArgs = [
            args[0],
            args[1],
            args[2],
            qlu.getDayCountBasis(args[3]),
            qlu.getCompoundType(args[4]),
            qlu.getFrequency(args[5])
        ]

        if len(args) > 6:
            newArgs.append(dfs.toQLDate(args[6]))

    return ql.BondFunctions.cleanPrice(*tuple(newArgs))


# =======================================================
# static Real   dirtyPrice (const Bond &bond,
#      const InterestRate &yield,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   dirtyPrice (const Bond &bond,
#      Rate yield,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date())
# =======================================================
def dirtyPrice(*args):
    if isinstance(args[1], ql.InterestRate):
        newArgs = [
            args[0],
            args[1],
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    else:
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4]),
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))

    return ql.BondFunctions.dirtyPrice(*tuple(newArgs))


# =======================================================
# static Real   bps (const Bond &bond,
#      const InterestRate &yield,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   bps (const Bond &bond,
#      const YieldTermStructure &discountCurve,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   bps (const Bond &bond,
#      Rate yield,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date())
# =======================================================


def bps(*args):
    if isinstance(args[1], ql.YieldTermStructure):
        newArgs = [
            args[0],
            args[1],
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    elif isinstance(args[1], ql.InterestRate):
        newArgs = [
            args[0],
            args[1],
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    else:
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4]),
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))

    return ql.BondFunctions.bps(*tuple(newArgs))


# =======================================================
# static Rate   yield (const Bond &bond,
#      Real cleanPrice,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date(),
#      Real accuracy=1.0e-10,
#      Size maxIterations=100,
#      Rate guess=0.05)
# -------------------------------------------------------
# static Rate   yield (Solver solver,
#      const Bond &bond,
#      Real cleanPrice,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date(),
#      Real accuracy=1.0e-10,
#      Rate guess=0.05)
# =======================================================
def bondYield(*args):
    if isinstance(args[0], ql.Bond) or isinstance(args[0], qlx.BondDecorator):
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4])
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))
        if len(args) > 6:
            newArgs.append(args[6])
        if len(args) > 7:
            newArgs.append(args[7])
        if len(args) > 8:
            newArgs.append(args[8])
    else:
        newArgs = [
            args[0],
            args[1],
            args[2],
            qlu.getDayCountBasis(args[3]),
            qlu.getCompoundType(args[4]),
            qlu.getFrequency(args[5]),
        ]

        if len(args) > 6:
            newArgs.append(dfs.toQLDate(args[6]))
        if len(args) > 7:
            newArgs.append(args[7])
        if len(args) > 8:
            newArgs.append(args[8])
    return ql.BondFunctions.bondYield(*tuple(newArgs))


def xbondYield(method, *args):
    # if isinstance(args[0], ql.Bond):
    if isinstance(args[0], ql.Bond) or isinstance(args[0], qlx.BondDecorator):
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4])
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))
        if len(args) > 6:
            newArgs.append(args[6])
        if len(args) > 7:
            newArgs.append(args[7])
        if len(args) > 8:
            newArgs.append(args[8])
    else:
        newArgs = [
            args[0],
            args[1],
            args[2],
            qlu.getDayCountBasis(args[3]),
            qlu.getCompoundType(args[4]),
            qlu.getFrequency(args[5]),
        ]

        if len(args) > 6:
            newArgs.append(dfs.toQLDate(args[6]))
        if len(args) > 7:
            newArgs.append(args[7])
        if len(args) > 8:
            newArgs.append(args[8])
    func = getattr(ql.BondFunctions, method)
    return func(*tuple(newArgs))


# =======================================================
# static Time   duration (const Bond &bond,
#      const InterestRate &yield,
#      Duration::Type type=Duration::Modified,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Time   duration (const Bond &bond,
#      Rate yield,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Duration::Type type=Duration::Modified,
#      Date settlementDate=Date())
# =======================================================

def duration(*args):
    if isinstance(args[1], ql.InterestRate):
        newArgs = [
            args[0],
            args[1]
        ]

        if len(args) > 2:
            newArgs.append(args[2])
        if len(args) > 3:
            newArgs.append(dfs.toQLDate(args[3]))
    else:
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4])
        ]

        if len(args) > 5:
            newArgs.append(args[5])
        if len(args) > 6:
            newArgs.append(dfs.toQLDate(args[6]))

    return ql.BondFunctions.duration(*tuple(newArgs))


# =======================================================
# static Real   convexity (const Bond &bond,
#      const InterestRate &yield,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   convexity (const Bond &bond,
#      Rate yield,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date())
# =======================================================

def convexity(*args):
    if isinstance(args[1], ql.InterestRate):
        newArgs = [
            args[0],
            args[1]
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    else:
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4])
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))

    return ql.BondFunctions.convexity(*tuple(newArgs))


# =======================================================
# static Real   basisPointValue (const Bond &bond,
#      const InterestRate &yield,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   basisPointValue (const Bond &bond,
#      Rate yield,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date())
# =======================================================

def basisPointValue(*args):
    if isinstance(args[1], ql.InterestRate):
        newArgs = [
            args[0],
            args[1]
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    else:
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4])
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))

    return ql.BondFunctions.basisPointValue(*tuple(newArgs))


# =======================================================
# static Real   yieldValueBasisPoint (const Bond &bond,
#      const InterestRate &yield,
#      Date settlementDate=Date())
# -------------------------------------------------------
# static Real   yieldValueBasisPoint (const Bond &bond,
#      Rate yield,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date())
# =======================================================
def yieldValueBasisPoint(*args):
    if isinstance(args[1], ql.InterestRate):
        newArgs = [
            args[0],
            args[1]
        ]

        if len(args) > 2:
            newArgs.append(dfs.toQLDate(args[2]))
    else:
        newArgs = [
            args[0],
            args[1],
            qlu.getDayCountBasis(args[2]),
            qlu.getCompoundType(args[3]),
            qlu.getFrequency(args[4])
        ]

        if len(args) > 5:
            newArgs.append(dfs.toQLDate(args[5]))

    return ql.BondFunctions.yieldValueBasisPoint(*tuple(newArgs))


# =======================================================
# static Spread     zSpread (const Bond &bond,
#      Real cleanPrice,
#      const boost::shared_ptr<YieldTermStructure> &,
#      const DayCounter &dayCounter,
#      Compounding compounding,
#      Frequency frequency,
#      Date settlementDate=Date(),
#      Real accuracy=1.0e-10,
#      Size maxIterations=100,
#      Rate guess=0.0)
# =======================================================
def zSpread(*args):
    newArgs = [
        args[0],
        args[1],
        args[2],
        qlu.getDayCountBasis(args[3]),
        qlu.getCompoundType(args[4]),
        qlu.getFrequency(args[5])
    ]

    if len(args) > 6:
        newArgs.append(dfs.toQLDate(args[6]))
    if len(args) > 7:
        newArgs.append(args[7])
    if len(args) > 8:
        newArgs.append(args[8])
    if len(args) > 9:
        newArgs.append(args[9])
    # for i, a in enumerate(newArgs):
    #     print('%d: %s, %s' % (i, type(a), a))
    return ql.BondFunctions.zSpread(*tuple(newArgs))


def yieldBisection(*args):
    return xbondYield('yieldBisection', *args)


def yieldBrent(*args):
    return xbondYield('yieldBrent', *args)


def yieldFalsePosition(*args):
    return xbondYield('yieldFalsePosition', *args)


def yieldNewton(*args):
    return xbondYield('yieldNewton', *args)


def yieldNewtonSafe(*args):
    return xbondYield('yieldNewtonSafe', *args)


def yieldRidder(*args):
    return xbondYield('yieldRidder', *args)


def yieldSecant(*args):
    return xbondYield('yieldSecant', *args)
