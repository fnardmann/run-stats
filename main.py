import fitparse
import glob
import matplotlib.pyplot as plt
import numpy as np
import datetime
from tqdm import tqdm

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
    return month_ticks(months, timestamps[0]), month_labels(months)

def month_ticks(months, first_ts):
    # create ticks with days from first timestamp
    return [(x - first_ts).days for x in months if x > x1]

def month_labels(months):
    month_dict = {
    1 : "Jan", 2 : "Feb", 3 : "Mar", 4 : "Apr",
    5 : "May", 6 : "Jun", 7 : "Jul", 8 : "Aug",
    9 : "Sep", 10 : "Oct", 11 : "Nov", 12 : "Dec" }

    return [month_dict[x.month] for x in months if x > x1]

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

standard_fields = ['total_distance', 'start_time', 'enhanced_avg_speed']
extra_fields = ['avg_heart_rate']

interval_data_collection = IntervalDataCollection()
interval_distance = 400.0

files = glob.glob("activities/*.fit")

for file in tqdm(files, total=len(files)):

    # Load the FIT file
    fitfile = fitparse.FitFile(file)

    lap_data = extract_lap(fitfile, standard_fields + extra_fields)

    lap_distance = lap_data['total_distance']
    lap_speed = lap_data['enhanced_avg_speed']

    interval_data = IntervalData(lap_data['start_time'][0].date())

    # filter interval laps and convert from m/s to min/km
    lap_speed = lap_speed[lap_distance == interval_distance]
    interval_data.data['pace'] = tominkm(lap_speed)

    # filter extra fields and append to collection
    for field in extra_fields:
        lap_data[field] = lap_data[field][lap_distance == interval_distance]
        interval_data.data[field] = lap_data[field]

    interval_data_collection.add(interval_data)

# sort interval and times according to times
interval_data_collection.sort()

timestamps = interval_data_collection.get_timestamps()
paces = interval_data_collection.get_data('pace')
heartrates = interval_data_collection.get_data_mean('avg_heart_rate')

x1 = timestamps[0]
x2 = timestamps[-1]
pos = [(x - x1).days for x in timestamps]

fig, ax = plt.subplots()

# gray background with white lines
ax.set_facecolor('lightgray')
ax.set_axisbelow(True)
plt.grid(color='w', linestyle='solid')

boxplots = ax.boxplot(paces, vert=True, positions=pos, widths=5, patch_artist=True)

# customize boxplots
for box in boxplots['boxes']:
    box.set(color='black', linewidth=1) # outline color
    box.set(facecolor='steelblue') # fill color

for median in boxplots['medians']:
    median.set(color='navy', linewidth=1)

ticks, labels = month_ticks_labels(timestamps)

ax.set_xticks(ticks)
ax.set_xticklabels(labels)
ax.set_xlim([-5, (x2-x1).days + 5])

ax.set_axisbelow(True)
pacesteps = (1/6)
ax.set_yticks(np.arange(3.0, 4.1, pacesteps))
ax.set_yticklabels(["3:00", "3:10", "3:20", "3:30", "3:40", "3:50", "4:00"])
ax.set_ylim([3.0 - 0.5 * pacesteps, 4.0 + 0.5 * pacesteps])
ax.invert_yaxis() # invert y axis because lower min/km means faster

ax.set_title('Interval Tracker')
ax.set_xlabel('Time')
ax.set_ylabel('Pace [min/km]')

# separate y axis for heartrate
hax = ax.twinx() 
hax.plot(pos, heartrates, c='darkred')
hrsteps = 4
hax.set_yticks(np.arange(156, 182, hrsteps))
hax.set_ylim([156 - 0.5 * hrsteps, 180 + 0.5 * hrsteps])
hax.set_ylabel('Heartrate [b/min]')

plt.show()