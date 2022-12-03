import fitparse
import glob
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def tominkm(speeds):
    """ Convert from m/s to min/km """
    speeds = speeds * 60 * 60 / 1000 # km/h
    speeds = np.divide(3600, speeds, out=np.zeros_like(speeds), where=speeds!=0)
    return speeds / 60 # min/km

intervals = []

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

    # ignore None values for speeds and filter laps
    lap_speed = lap_speed[lap_speed != None]
    lap_intervals = lap_speed[lap_distance == 400.0]

    # speed values are stored in m/s
    lap_intervals = tominkm(lap_intervals)

    # store (date, interval) tuple
    intervals.append((timestamps[0].date(), lap_intervals))

# sort interval and times according to times
times, intervals = zip(*sorted(intervals, key=lambda pair: pair[0]))

x1 = times[0]
x2 = times[-1]
pos = [(x - x1).days for x in times]

fig, ax = plt.subplots()
ax.boxplot(intervals, vert=True, positions=pos)
ax.set_xlim([0, (x2-x1).days])
ax.set_xticklabels(times)

# invert y axis because lower min/km means faster
ax.invert_yaxis()

plt.show()