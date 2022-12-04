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

intervals = []
warmups = []

files = glob.glob("activities/*.fit")

for file in tqdm(files, total=len(files)):

    # Load the FIT file
    fitfile = fitparse.FitFile(file)

    lap_distance, lap_speed, timestamps = [], [], []

    # Iterate over all messages of type "record"
    # (other types include "device_info", "file_creator", "event", etc)
    for record in fitfile.get_messages('lap'):

        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in record:
            if data.name == 'enhanced_avg_speed':
                lap_speed.append(data.value)
            if data.name == 'total_distance':
                lap_distance.append(data.value)
            if data.name == 'start_time':
                timestamps.append(data.value)


    lap_speed = np.array(lap_speed)
    lap_distance = np.array(lap_distance)

    # sum up distances until first interval is reached
    warmup_distance = 0
    for x in lap_distance:
        if x == 400.0: break
        warmup_distance += x
    warmups.append(warmup_distance)

    # ignore None values for speeds and filter laps
    lap_speed = lap_speed[lap_speed != None]
    lap_intervals = lap_speed[lap_distance == 400.0]

    # speed values are stored in m/s
    lap_intervals = tominkm(lap_intervals)

    # store (date, interval) tuple
    intervals.append((timestamps[0].date(), lap_intervals))

print(warmups)

# sort interval and times according to times
times, intervals = zip(*sorted(intervals, key=lambda pair: pair[0]))

x1 = times[0]
x2 = times[-1]
pos = [(x - x1).days for x in times]

fig, ax = plt.subplots()

# gray background with white lines
ax.set_facecolor('#E6E6E6')
ax.set_axisbelow(True)
plt.grid(color='w', linestyle='solid')

boxplots = ax.boxplot(intervals, vert=True, positions=pos, widths=5, patch_artist=True)

# customize boxplots
for box in boxplots['boxes']:
    box.set(color='black', linewidth=1) # outline color
    box.set(facecolor='#EE6666') # fill color

for median in boxplots['medians']:
    median.set(color='darkred', linewidth=1)


# get months of existing range and use them as ticks
months = []
month = datetime.date(times[0].year, times[0].month, 1)
while month < times[-1]:
    months.append(month)
    # advance one month
    new_year = month.year
    new_month = month.month + 1
    if new_month > 12:
        new_year += 1
        new_month -= 12
    month = datetime.date(new_year, new_month, 1)

month_dict = {
    1 : "Jan", 2 : "Feb", 3 : "Mar", 4 : "Apr",
    5 : "May", 6 : "Jun", 7 : "Jul", 8 : "Aug",
    9 : "Sep", 10 : "Oct", 11 : "Nov", 12 : "Dec" }

ticks = [(x - x1).days for x in months if x > x1]
labels = [month_dict[x.month] for x in months if x > x1]

ax.set_xticks(ticks)
ax.set_xticklabels(labels)
ax.set_xlim([-5, (x2-x1).days + 5])

ax.set_axisbelow(True)
ax.set_yticks([3.0, 3.167, 3.333, 3.5, 3.667, 3.833, 4.0])
ax.set_yticklabels(["3:00", "3:10", "3:20", "3:30", "3:40", "3:50", "4:00"])
ax.set_ylim([2.95, 4.05])
ax.invert_yaxis() # invert y axis because lower min/km means faster

ax.set_title('Interval Tracker')
ax.set_xlabel('Time')
ax.set_ylabel('Pace [min/km]')

plt.show()