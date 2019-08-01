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

import os
import json
import QuantLib as ql
from pathlib import Path

config = None


def getThisDir():

    # mypath = Path().absolute()
    path = Path(__file__).parent.absolute()
    return path


def getConfigDir():
    p = getThisDir()
    tmp = os.path.split(p)

    return os.path.join(tmp[0], 'config')


def trimSuffix(xstring, suffix):
    xstring = xstring.upper()

    if xstring.endswith(suffix):
        sz = len(suffix)
        xstring = xstring[:-sz]

    return xstring


def getMap(table):
    global config
    table = table.upper()
    if config is None:
        # cwd = os.getcwd()
        # print(cwd)
        configDir = getConfigDir()
        fileName = os.path.join(configDir, "QuantLibConfig.json")
        with open(fileName) as jsonFile:
            # print("Loading ...")
            config = json.load(jsonFile)

    # if config is None:
    #                 print("config is none")

    if table not in config:
        raise ValueError("Invalid table ID: %s" % table)

    return config[table]


def getValue(table, name, msg):
    if not isinstance(name, str):
        name = str(name)
    nvp = getMap(table)
    name = name.upper()
    if name not in nvp:
        raise ValueError("Invalid %s ID:%s, not found in table %s" %
                         (msg, name, table))

    return nvp[name]


def getRef(table, key, msg):
    if not isinstance(key, str):
        return key

    val = getValue(table, key, msg)
    ref = getattr(ql, val)
    return ref


def getObject(table, key, msg):
    if not isinstance(key, str):
        return key

    className = getValue(table, key, msg)
    clazz = getattr(ql, className)
    return clazz()


def getCurrency(ccy):
    return getObject('CCY_MAP', ccy, 'currency')


def getFrequency(freq):
    if isinstance(freq, int):
        return freq
    return getRef('FREQUENCY_MAP', str(freq), 'frequency')


def parseTenor(tenor):
    if isinstance(tenor, ql.Period):
        return tenor

    if tenor.upper() == 'OTHERFREQUENCY':
        raise RuntimeError('Unknown period:%s' % tenor)

    nvp = getMap('FREQUENCY_MAP')
    if tenor.upper() in nvp:
        propertyName = nvp[tenor.upper()]
        ref = getattr(ql, propertyName)
        return ql.Period(ref)

    tenor = tenor.upper().strip()
    pos = 0
    years = 0
    months = 0
    weeks = 0
    days = 0
    for i, c in enumerate(tenor):
        if c in "YMWD":
            # print("...........", tenor[pos:i], ',', tenor)
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


def getTenor(name):
    if not isinstance(name, str):
        return name

    return ql.Period(getFrequency(name))


def getRollingConv(name):
    if not isinstance(name, str):
        return name
    if name.lower() == 'none':
        return None

    return getRef('ROLL_CONV_MAP', name, 'rolling convention')


def getDayCountBasis(name):
    return getObject('DAY_COUNT_MAP', name, 'day count basis')


def getDateGenRule(name):
    if name is None:
        return None

    if not isinstance(name, str):
        return name

    if name.lower() == 'none':
        return None

    val = getValue('DATE_GEN_FLAG', name, 'day generation rule')
    tmp = val.split('.')
    ref = getattr(ql, tmp[0])
    rule = getattr(ref, tmp[1])
    return rule


def getPositionType(ptype):
    if ptype is None:
        raise RuntimeError(
            "Position type can only be long or short. It cannot be None")

    if isinstance(ptype, int) and ptype >= 0 and ptype <= 1:
        return ptype

    if not isinstance(ptype, str):
        raise RuntimeError("Invalid position type")

    val = getValue('POSITION', ptype, 'position type')
    tmp = val.split('.')
    ref = getattr(ql, tmp[0])
    return getattr(ref, tmp[1])


def getCompoundType(ctype):
    if isinstance(ctype, int):
        return ctype

    ctype = str(ctype)

    return getRef('COMPOUNDING_MAP', ctype, 'day compounding type')


def getVolitiliryType(name):
    return getRef('VOLATILITY_TYPE_MAP', name, 'volitility type')


def getJointCalRule(name):
    return getRef('JOINT_CALENDAR_RULE_MAP', name, 'joint calendar rule')


def getInterpolation(key):
    return getObject('INTERPOLATION_MAP', key, 'interpolation')


def getInterpolationMethod(key):
    return getObject('INTERPOLATION_METHOD_MAP', key, 'interpolation')


def getMarketIndex(key):
    temp = key.split(',')
    ref = getRef('MARKET_INDEX_MAP', temp[0].strip(), 'market index')
    if len(temp) == 1:
        return ref()
    else:
        tenor = parseTenor(temp[1].strip())
        # print(tenor, type(tenor))
        return ref(tenor)


def getTermStructureHandle(key):
    if not isinstance(key, str):
        return key

    key = trimSuffix(key.upper(), "TERMSTRUCTUREHANDLE")
    key = trimSuffix(key, "TERMSTRUCTURE")

    return getObject('TERM_STRUCTURE_HANDLE_MAP', key, 'term structure handle')


def getTermStructure(key):
    if not isinstance(key, str):
        return key

    key = trimSuffix(key.upper(), "TERMSTRUCTURE")

    return getObject('TERM_STRUCTURE_MAP', key, 'term structure')


def getPricingEngine(key, curveHandle=None):
    if not isinstance(key, str):
        return key

    key = trimSuffix(key.upper(), "ENGINE")
    ref = getRef('ENGINE_MAP', key, 'pricing engine')

    if curveHandle is None:
        return ref()
    else:
        return ref(curveHandle)


# def setEvalDate(dt):
#     ql.Settings.instance().evaluationDate = toQLDate(dt)
