# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
REF: pip install xlrd
     Library for developers to extract data from Microsoft Excel (tm) spreadsheet files
"""

import datetime as datetime
import QuantLib as ql
# from . import QuantLibUtils

TIME_UNIT_MAP = {
    'D': ql.Days,
    'W': ql.Weeks,
    'M': ql.Months,
    'Y': ql.Years,
    'DAYS': ql.Days,
    'WEEKS': ql.Weeks,
    'MONTHS': ql.Months,
    'YEARS': ql.Years,
    'HOURS': ql.Hours,
    'MINUTES': ql.Minutes,
    'SECONDS': ql.Seconds,
    'MILLISECONDS': ql.Milliseconds,
    'MICROSECONDS': ql.Microseconds
}

# The valid year range in QuantLib is [1901,2199]
# January 1st, 1901   serial: 367
# December 31st, 2199 serial: 109574


def isExcelSerial(dt):
    return dt is not None and isinstance(dt, int) and dt >= 367 and dt <= 109574

# The following is a rough test


def isYYYYMMDD(dt):
    if dt is None or not isinstance(dt, int):
        return False

    dd = dt % 100
    yyyymm = dt // 100
    mm = yyyymm % 100
    yyyy = yyyymm // 100

    return yyyy >= 1901 and yyyy <= 2199 and mm >= 1 and mm <= 12 and dd >= 1 and dd <= 31


def getTimeUnit(name):
    name = name.upper()
    if name not in TIME_UNIT_MAP:
        raise ValueError("Invalid time unit:%s" % name)

    return TIME_UNIT_MAP[name]


def xlserial2datetime(xldate):
    tempDate = datetime.datetime(1899, 12, 30)  # 1900,1,1
    deltaDays = datetime.timedelta(days=int(xldate))
    secs = (int((xldate % 1) * 86400))  # -60
    detlaSeconds = datetime.timedelta(seconds=secs)
    theTime = (tempDate + deltaDays + detlaSeconds)
    # return TheTime.strftime("%Y-%m-%d %H:%M:%S")
    return theTime


def datetime2xlserial(dt):
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = dt - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


def datetime2yyyymmdd(dt):
    if isinstance(dt, datetime.datetime):
        return dt.year * 10000 + dt.month * 100 + dt.day
    else:
        raise ValueError("Invalid datetime")


def yyyymmdd2datetime(yyyymmdd):
    dd = yyyymmdd % 100
    yyyymm = yyyymmdd // 100
    mm = yyyymm % 100
    yyyy = yyyymm // 100
    return datetime.datetime(yyyy, mm, dd)


def xlserial2yyyymmdd(serial):
    dt = xlserial2datetime(serial)
    yyyymmdd = dt.year * 10000 + dt.month * 100 + dt.day
    return yyyymmdd


def yyyymmdd2xlserial(yyyymmdd):
    dt = yyyymmdd2datetime(yyyymmdd)
    return datetime2xlserial(dt)


def number2yyyymmdd(nbr):
    nbr = int(nbr)
    if nbr > 19000101:
        dd = nbr % 100
        mm = (nbr // 100) % 100
        if dd < 1 or dd > 31 or mm < 1 or mm > 12:
            raise ValueError('Invalid yyyymmdd.')
    else:
        nbr = int(xlserial2yyyymmdd(nbr))
    return nbr


def number2xlserial(nbr):
    nbr = int(nbr)
    if nbr > 19000101:
        dd = nbr % 100
        mm = (nbr // 100) % 100
        if dd < 1 or dd > 31 or mm < 1 or mm > 12:
            raise ValueError('Invalid yyyymmdd.')
        nbr = yyyymmdd2xlserial(nbr)
    return nbr


def number2datetime(nbr):
    xlserial = number2xlserial(nbr)
    return xlserial2datetime(xlserial)


def qldate2yyyymmdd(dt):
    if dt is isinstance(dt, ql.Date):
        return dt

    return dt.year() * 10000 + dt.month() * 100 + dt.dayOfMonth()


def number2ymd(nbr):
    yyyymmdd = number2yyyymmdd(nbr)
    d = yyyymmdd % 100
    yyyymm = yyyymmdd // 100
    m = yyyymm % 100
    y = yyyymm // 100
    return (y, m, d)


def number2qldate(nbr):
    y, m, d = number2ymd(nbr)
    return ql.Date(d, m, y)


def toQLDate(dt):
    if isinstance(dt, ql.Date):
        return dt
    else:
        return number2qldate(dt)


def addDaysAsQLDate(dtNbr, nbDays):
    dt = number2qldate(dtNbr)
    dt = dt + ql.Period(nbDays, ql.Days)
    return dt


def addDaysAsXlSerial(dtNbr, nbDays):
    dt = addDaysAsQLDate(dtNbr, nbDays)
    return dt.serialNumber()


def addDaysAsYYYYMMDD(dtNbr, nbDays):
    dt = addDaysAsQLDate(dtNbr, nbDays)
    return qldate2yyyymmdd(dt)


def addWeeksAsQLDate(dtNbr, nbWeeks):
    dt = number2qldate(dtNbr)
    dt = dt + ql.Period(nbWeeks, ql.Weeks)
    return dt


def addWeeksAsXlSerial(dtNbr, nbWeeks):
    dt = addWeeksAsQLDate(dtNbr, nbWeeks)
    return dt.serialNumber()


def addWeeksAsYYYYMMDD(dtNbr, nbWeeks):
    dt = addWeeksAsQLDate(dtNbr, nbWeeks)
    return qldate2yyyymmdd(dt)


def addMonthsAsQLDate(dtNbr, nbrMonths):
    dt = number2qldate(dtNbr)
    dt = dt + ql.Period(nbrMonths, ql.Months)
    return dt


def addMonthsAsXlSerial(dtNbr, nbrMonths):
    dt = addMonthsAsQLDate(dtNbr, nbrMonths)
    return dt.serialNumber()


def addMonthsAsYYYYMMDD(dtNbr, nbrMonths):
    dt = addMonthsAsQLDate(dtNbr, nbrMonths)
    return qldate2yyyymmdd(dt)


def addYearsAsQLDate(dtNbr, nbrYears):
    dt = number2qldate(nbrYears)
    dt = dt + ql.Period(nbrYears, ql.Months)
    return dt


def addYearsAsXlSerial(dtNbr, nbrYears):
    dt = addYearsAsQLDate(dtNbr, nbrYears)
    return dt.serialNumber()


def addYearsAsYYYYMMDD(dtNbr, nbrYears):
    dt = addYearsAsQLDate(dtNbr, nbrYears)
    return qldate2yyyymmdd(dt)


def addYMWDAsQLDate(dtNbr, nbrYears, nbrMonths, nbrWeeks, nbrDays):
    dt = number2qldate(dtNbr)
    dt = dt + ql.Period(nbrYears, ql.Years)
    dt = dt + ql.Period(nbrMonths, ql.Months)
    dt = dt + ql.Period(nbrWeeks, ql.Weeks)
    dt = dt + ql.Period(nbrDays, ql.Days)
    return dt


def addYMWDAsXlSerial(dtNbr, nbrYears, nbrMonths, nbrWeeks, nbrDays):
    dt = addYMWDAsQLDate(dtNbr, nbrYears, nbrMonths, nbrWeeks, nbrDays)
    return dt.serialNumber()


def addYMWDAsYYYYMMDD(dtNbr, nbrYears, nbrMonths, nbrWeeks, nbrDays):
    dt = addYMWDAsQLDate(dtNbr, nbrYears, nbrMonths, nbrWeeks, nbrDays)
    return qldate2yyyymmdd(dt)


def tenor2period(tenor):
    tenor = tenor.upper()
    p = None
    if tenor.endswith('D') or tenor.endswith('W') or tenor.endswith('M') or tenor.endswith('Y'):
        amt = int(tenor[:len(tenor) - 1])
        unit = tenor[-1:]
        # print("%s %s" % (amt, unit))
        p = ql.Period(amt, getTimeUnit(unit))
        # print(p)
    return p


def parseTenor(tenor):
    tenor = tenor.upper().strip()
    if tenor == 'NONE':
        return None

    pos = 0
    years = 0
    months = 0
    weeks = 0
    days = 0
    for i, c in enumerate(tenor):
        if c in "YMWD":
            nbr = int(tenor[pos:i])
            pos = i + 1
            if c == 'Y':
                years = nbr
            elif c == 'M':
                months = nbr
            elif c == 'W':
                weeks = nbr
            else:
                days = nbr

    if years > 0 and months:  # convert to months
        months += years * 12
        years = 0

    p = None
    if years > 0:
        p = ql.Period(years, ql.Years)
    elif months > 0:
        p = ql.Period(months, ql.Months)
    elif weeks > 0:
        p = ql.Period(weeks, ql.Weeks)
    else:
        p = ql.Period(days, ql.Days)

    return p
