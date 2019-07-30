import os
from pathlib import Path


def getCurrentDir():
    path = Path(__file__).parent.absolute()
    return path


def getParentDir():
    # get the absolute path to the current file
    path = Path(__file__).parent.absolute()
    # split it and drop the last directory
    tmp = os.path.split(path)
    return tmp[0]


def getCurveDir():
    configDir = os.getenv('CURVE_DIR', None)
    if configDir is None:
        configDir = os.path.join(getParentDir(), 'curves')

    return configDir


def getCurveInputFile(fileName):
    inputDir = os.path.join(getCurveDir(), 'input')
    return os.path.join(inputDir, fileName)


def getConfigDir():
    configDir = os.getenv('CONFIG_DIR', None)
    if configDir is None:
        configDir = os.path.join(getParentDir(), 'config')

    return configDir


def getCalendarDir():
    calDir = os.getenv('CALENDAR_DIR', None)
    if calDir is None:
        calDir = os.path.join(getParentDir(), 'calendars')

    return calDir


def getCalendarIndexURL():
    url = 'file:///' + os.path.join(getConfigDir(), 'Calendar.idx')
    return url


def getScheduleConfigURL():
    url = 'file:///' + os.path.join(getConfigDir(), 'ScheduleConfig.json')
    return url

# https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python/3430395
# try:
#     # For Python 3.0 and later
#     from urllib.request import urlopen
# except ImportError:
#     # Fall back to Python 2's urllib2
#     from urllib2 import urlopen

# try:
#     # for Python 2.x
#     from StringIO import StringIO
# except ImportError:
#     # for Python 3.x
#     from io import StringIO
# import csv

# def loadCalendarFile(calName, calUrl):
#     if calUrl.startswith('file:') or calUrl.startswith('http:') or calUrl.startswith('https:'):
#         url = calUrl
#     else:
#         url = 'file:///' + os.path.join(getCalendarDir(), calUrl)

#     res = urlopen(url)
#     content = res.read()
#     content = content.decode("utf-8")
#     f = StringIO(content)
#     reader = csv.reader(f, delimiter=',')

#     return reader


# def loadCalendarIndex():
#     url = getCalendarIndexURL()
#     res = urlopen(url)
#     content = res.read()
#     content = content.decode("utf-8")
#     f = StringIO(content)
#     reader = csv.reader(f, delimiter=',')
#     idx = {}
#     # skip the first two rows
#     next(reader)
#     next(reader)
#     for row in reader:
#         idx[row[0].strip().upper()] = (row[1].strip(), row[2].strip())

#     return idx
