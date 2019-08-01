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
