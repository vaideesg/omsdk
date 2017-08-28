from datetime import datetime, timedelta, date
import time

class SchTimer:
    def __init__(self, time_str = None, fmt ="%Y-%m-%d", untilmin=24*60):
        if time_str is None:
            self.time = datetime.now()
        else:
            self.time = datetime.strptime(time_str, fmt)
        self.until = None
        if untilmin is not None:
            self.until = self.time + timedelta(minutes=untilmin)

    def __str__(self):
        mystr = "Time: "+ str(self.time)
        if self.until is not None:
            mystr = mystr + "; Until: "+ str(self.until)
        return mystr

TIME_NOW = SchTimer(time_str = "1970-1-1", untilmin=None)
