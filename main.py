import fitparse
import glob
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import utils
from utils import IntervalData, IntervalDataCollection

standard_fields = ['total_distance', 'start_time', 'enhanced_avg_speed']
extra_fields = ['avg_heart_rate']

interval_data_collection = IntervalDataCollection()
interval_distance = 400.0

files = glob.glob("activities/*.fit")

for file in tqdm(files, total=len(files)):

    # Load the FIT file
    fitfile = fitparse.FitFile(file)

    lap_data = utils.extract_lap(fitfile, standard_fields + extra_fields)

    lap_distance = lap_data['total_distance']
    lap_speed = lap_data['enhanced_avg_speed']

    interval_data = IntervalData(lap_data['start_time'][0].date())

    # filter interval laps and convert from m/s to min/km
    lap_speed = lap_speed[lap_distance == interval_distance]
    interval_data.data['pace'] = utils.tominkm(lap_speed)

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

ticks, labels = utils.month_ticks_labels(timestamps)

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