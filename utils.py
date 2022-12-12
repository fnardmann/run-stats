import datetime
import numpy as np

def tominkm(speeds):
    """ Convert from m/s to min/km """
    speeds = speeds * 60 * 60 / 1000 # km/h
    speeds = np.divide(3600, speeds, out=np.zeros_like(speeds), where=speeds!=0)
    return speeds / 60 # min/km


def extract_lap(fitfile, fields):
    """ Extract lap information of this fitfile """
    # dictionary to collect data
    # key: name, value: data records
    datadict = {}

    # every field represents a data record to be extracted
    for field in fields:
        datadict[field] = []

    # Iterate over all messages of type "record"
    # (other types include "device_info", "file_creator", "event", etc)
    for record in fitfile.get_messages('lap'):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in record:
            for field in fields:
                if data.name == field:
                    datadict[field].append(data.value)

    # convert to numpy array and ignore None values
    for key, value in datadict.items():
        value = np.array(value)
        datadict[key] = value[value != None]
    
    return datadict

def months_in_range(first_ts, last_ts):
    # get months of existing range and use them as ticks
    months = []
    month = datetime.date(first_ts.year, first_ts.month, 1)
    while month < last_ts:
        months.append(month)
        # advance one month
        new_year = month.year
        new_month = month.month + 1
        if new_month > 12:
            new_year += 1
            new_month -= 12
        month = datetime.date(new_year, new_month, 1)
    return months

def month_ticks_labels(timestamps):
    months = months_in_range(timestamps[0], timestamps[-1])
    return month_ticks(months, timestamps[0]), month_labels(months, timestamps[0])

def month_ticks(months, first_ts):
    # create ticks with days from first timestamp
    return [(x - first_ts).days for x in months if x > first_ts]

def month_labels(months, first_ts):
    month_dict = {
    1 : "Jan", 2 : "Feb", 3 : "Mar", 4 : "Apr",
    5 : "May", 6 : "Jun", 7 : "Jul", 8 : "Aug",
    9 : "Sep", 10 : "Oct", 11 : "Nov", 12 : "Dec" }

    return [month_dict[x.month] for x in months if x > first_ts]

class IntervalData:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.data = {}

class IntervalDataCollection:
    def __init__(self):
        self.collection = []
    
    def add(self, interval_data):
        self.collection.append(interval_data)

    def sort(self):
        self.collection = sorted(self.collection, key=lambda d: d.timestamp)

    def get_timestamps(self):
        return [d.timestamp for d in self.collection]

    def get_data(self, field):
        return [d.data[field] for d in self.collection]

    def get_data_mean(self, field):
        return [np.mean(d) for d in self.get_data(field)]