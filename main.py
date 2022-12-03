import fitparse
import glob
import matplotlib.pyplot as plt
import numpy as np

def tominkm(speeds):
    """ Convert from m/s to min/km """
    speeds = speeds * 60 * 60 / 1000 # km/h
    speeds = np.divide(3600, speeds, out=np.zeros_like(speeds), where=speeds!=0)
    return speeds / 60 # min/km

files = glob.glob("activities/*.fit")

for file in files:

    # Load the FIT file
    fitfile = fitparse.FitFile(file)

    lap_speed = []
    lap_distance = []
    

    # Iterate over all messages of type "record"
    # (other types include "device_info", "file_creator", "event", etc)
    for record in fitfile.get_messages('lap'):

        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in record:
            if data.name == 'enhanced_avg_speed':
                lap_speed.append(data.value)
            if data.name == 'total_distance':
                lap_distance.append(data.value)


    lap_speed = np.array(lap_speed)
    lap_distance = np.array(lap_distance)

    # ignore None values for speeds
    lap_speed = lap_speed[lap_speed != None]

    intervals = lap_speed[lap_distance == 400.0]

    # speed values are stored in m/s
    intervals = tominkm(intervals)

    print(intervals)

    break