class ScheduleLoader(object):
    """docstring for ScheduleLoader"""

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def load(self, prodId):
        raise RuntimeError(
            "This is the super class of all schedule loaders, please use any concret one")
