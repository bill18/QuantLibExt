import QuantLib as ql
from . import QuantLibUtils as qlu
from . import DatetimeUtils as dfs
from . import CalendarManager as mgr


def oneDayForwardRates(curve, period, calendar, startDate=None, dayCount=None, compounding=ql.Compounded, freq=ql.Annual):
    startDate = startDate if startDate is not None else curve.referenceDate()
    startDate = startDate if isinstance(
        startDate, ql.Date) else dfs.toQLDate(startDate)
    period = period if isinstance(
        period, ql.Period) else qlu.parseTenor(period)
    endDate = startDate + period
    if dayCount is None:
        dayCount = curve.dayCounter()
    else:
        dayCount = dayCount if isinstance(
            dayCount, ql.DayCounter) else qlu.getDayCountBasis(dayCount)
    dates = [ql.Date(serial)
             for serial
             in range(startDate.serialNumber(), endDate.serialNumber() + 1)]

    if calendar is None:
        raise RuntimeError('You must provide a calendar')

    if calendar is None:
        calendar = curve.calendar()
    else:
        calendar = calendar if isinstance(
            calendar, ql.Calendar) else mgr.getCalendar(calendar)

    rates = [curve.forwardRate(d,
                               calendar.advance(d, 1, ql.Days), dayCount, compounding, freq).rate()
             for d in dates]

    return {'dates': dates, 'rates': rates}
