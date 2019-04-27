from datetime import datetime
from time import gmtime, strftime
from pytz import timezone
import pytz

#get time
def getTime():
    date_format='%H:%M:%S'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    return date.strftime(date_format)

def timeDifference(value2, value1):
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(value2, FMT) - datetime.strptime(value1, FMT)
    return tdelta
