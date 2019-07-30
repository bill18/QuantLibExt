class CalendarLoader(object):
    """docstring for CalendarLoader"""

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def load(self, calId):
        raise RuntimeError(
            "This is the super class of all calendar loaders, please use any concret one")
