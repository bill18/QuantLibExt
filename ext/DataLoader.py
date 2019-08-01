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


class DataLoader(object):
    """docstring for DataLoader"""

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def load(self, calId):
        raise RuntimeError(
            "This is the super class of all data loaders (calendar/schedule/curve, etc), please use any concret one")
