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

"""
The test data was extracted from:
http://gouthamanbalaraman.com/blog/value-treasury-futures-quantlib-python.html

"""
import QuantLib as ql
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import FuncFormatter
import ext.Config as config
import ext.QuantLibClassExt as qlx
import ext.CurveBuilder as builder
import ext.BondFunctions as bfs
import ext.CurveUtils as cutil


def plot(lineType, dates, rates):
    pydt = [datetime.datetime(d.year(), d.month(), d.dayOfMonth())
            for d in dates]
    fig, ax = plt.subplots()
    fig.set_size_inches(10.5, 9.5)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda r, pos: '{:.2%}'.format(r)))
    plt.subplots_adjust(bottom=0.2)
    l, = plt.plot(pydt, rates, lineType)
    plt.show()


def plotCurve(curve):
    data = cutil.oneDayForwardRates(curve, '2Y', 'TGT', compounding='Simple')
    plot('.', **data)


def checkDiscountFactors(yield_curve):
    maturity_dates = [20151224,
                      20160225,
                      20160526,
                      20161110,
                      20171130,
                      20181115,
                      20201130,
                      20221130,
                      20251115,
                      20451115]
    for d in maturity_dates:
        print("|%20s  %9.6f|" % (d, yield_curve.discount(d)))


def testBond():
    calc_date = 20151130
    day_count = 'Act/Act'
    futures_price = 127.0625
    delivery_date = 20151201
    settlement_days = 0
    calendar = 'USD'
    compounding = "Compounded"
    coupon_frequency = "Semiannual"

    # instFileUrl = config.getCurveInputFile('bond.json')

    yield_curve = builder.PiecewiseCubicZeroCurve(
                                             calc_date, day_count, 'bond')

    deliverable = qlx.FixedRateBond(0,  # settlement_days
                                    100.0,  # face_value
                                    'TRY20251130',  # schedule ID
                                    [0.06],  # coupon_rate
                                    day_count,  # day count basis
                                    curve=yield_curve,
                                    engine='DiscountingBond'
                                    )

    # yield_curve_handle = ql.YieldTermStructureHandle(yield_curve)
    # bond_engine = ql.DiscountingBondEngine(yield_curve_handle)
    # deliverable.setPricingEngine(bond_engine)

    clean_price = futures_price * yield_curve.discount(delivery_date)

    zspread = bfs.zSpread(deliverable,
                          clean_price,
                          yield_curve,
                          day_count,
                          compounding,
                          coupon_frequency,
                          calc_date) * 10000

    print("Z-Spread =%3.0fbp" % (zspread))
    checkDiscountFactors(yield_curve)

# def createSampleSecurities(calc_date, futures_price, yield_curve, basis, day_count):
    #    bondId       , issue   , maturity, coupon  , price
    basket = [
        ("TRY20220815", 20120815, 20220815, 1.625000, 97.921875),
        ("TRY20221115", 20121115, 20221115, 1.625000, 97.671875),
        ("TRY20220930", 20120930, 20220930, 1.750000, 98.546875),
        ("TRY20230515", 20130515, 20230515, 1.750000, 97.984375),
        ("TRY20220831", 20120831, 20220831, 1.875000, 99.375000),
        ("TRY20221031", 20121031, 20221031, 1.875000, 99.296875),
        ("TRY20220731", 20120731, 20220731, 2.000000, 100.265625),
        ("TRY20230215", 20130215, 20230215, 2.000000, 100.062500),
        ("TRY20250215", 20150215, 20250215, 2.000000, 98.296875),
        ("TRY20250815", 20150815, 20250815, 2.000000, 98.093750),
        ("TRY20220630", 20120630, 20220630, 2.125000, 101.062500),
        ("TRY20250515", 20150515, 20250515, 2.125000, 99.250000),
        ("TRY20241115", 20141115, 20241115, 2.250000, 100.546875),
        ("TRY20251115", 20151115, 20251115, 2.250000, 100.375000),
        ("TRY20240815", 20140815, 20240815, 2.375000, 101.671875),
        ("TRY20230815", 20130815, 20230815, 2.500000, 103.250000),
        ("TRY20240515", 20140515, 20240515, 2.500000, 102.796875),
        ("TRY20231115", 20131115, 20231115, 2.750000, 105.062500),
        ("TRY20240215", 20140215, 20240215, 2.750000, 104.875000)
    ]

    yield_curve_handle = ql.YieldTermStructureHandle(yield_curve)
    ctd_cf = None
    min_basis = 100
    for i, b in enumerate(basket):
        bondId, issue, maturity, coupon, price = b
        # issue = maturity - ql.Period(10, ql.Years)
        s = qlx.FixedRateBond(settlement_days,  # settlement_days
                              100.0,  # face_value
                              bondId,  # schedule ID
                              [coupon / 100.],  # coupon_rate
                              day_count,  # day count basis
                              curve=yield_curve,
                              engine='DiscountingBond'
                              )
        # s = create_tsy_security(issue, maturity, coupon / 100.)
        # bond_engine = ql.DiscountingBondEngine(yield_curve_handle)
        # s.setPricingEngine(bond_engine)
        cf = bfs.cleanPrice(s,
                            0.06,
                            day_count,
                            compounding,
                            coupon_frequency,
                            calc_date) / 100.
        adjusted_futures_price = futures_price * cf
        basis = price - adjusted_futures_price
        if basis < min_basis:
            min_basis = basis
            ctd_bond = s
            ctd_cf = cf
            ctd_info = b

    ctd_price = ctd_info[4]
    print("%-30s = %lf" % ("Minimum Basis", min_basis))
    print("%-30s = %lf" % ("Conversion Factor", ctd_cf))
    print("%-30s = %lf" % ("Coupon", ctd_info[3]))
    print("%-30s = %s" % ("Maturity", ctd_info[2]))
    print("%-30s = %lf" % ("Price", ctd_info[4]))

    futures_maturity_date = 20151221
    bussiness_convention = 'F'
    futures = qlx.FixedRateBondForward(calc_date,
                                       futures_maturity_date,
                                       'Long',
                                       0.0,
                                       settlement_days,
                                       day_count,
                                       calendar,
                                       bussiness_convention,
                                       ctd_bond,
                                       yield_curve_handle,
                                       yield_curve_handle)

    model_futures_price = futures.cleanForwardPrice() / ctd_cf
    implied_yield = futures.impliedYield(ctd_price / ctd_cf,
                                         futures_price,
                                         calc_date,
                                         compounding,
                                         day_count).rate()
    z_spread = bfs.zSpread(ctd_bond,
                           ctd_price,
                           yield_curve,
                           day_count,
                           compounding,
                           coupon_frequency,
                           calc_date)

    ytm = bfs.bondYield(ctd_bond,
                        ctd_price,
                        day_count,
                        compounding,
                        coupon_frequency,
                        calc_date)

    print("%-30s = %lf" % ("Model Futures Price", model_futures_price))
    print("%-30s = %lf" % ("Market Futures Price", futures_price))
    print("%-30s = %lf" % ("Model Adjustment",
                           model_futures_price - futures_price))
    print("%-30s = %2.3f%%" % ("Implied Yield", implied_yield * 100))
    print("%-30s = %2.1fbps" % ("Forward Z-Spread", z_spread * 10000))
    print("%-30s = %2.3f%%" % ("Forward YTM ", ytm * 100))
    plotCurve(yield_curve)


# ===============================================================
# main function starts here ...
if __name__ == '__main__':
    testBond()
