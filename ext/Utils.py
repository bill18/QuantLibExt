import csv
import json

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO


def parseCSVString(s, delimiter=','):
    f = StringIO(s)
    return csv.reader(f, delimiter=delimiter)


def readFromUrl(url):
    res = urlopen(url)
    content = res.read()
    return content.decode("utf-8")


def loadJsonFromUrl(url):
    content = readFromUrl(url)
    return json.loads(content)


def loadCSVFromUrl(url, delimiter=','):
    content = readFromUrl(url)
    return parseCSVString(content, delimiter)
