import fitparse
import glob
import matplotlib.pyplot as plt
import numpy as np

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

    print(lap_speed)
    print(lap_distance)

    break
    
    # speed values are stored in m/s
    speeds = speeds * 60 * 60 / 1000 # km/h
    speeds = np.divide(3600, speeds, out=np.zeros_like(speeds), where=speeds!=0)
    speeds = speeds / 60 # min/km

    plt.gca().set_ylim([3, 8])
    plt.gca().invert_yaxis()

    x = range(len(speeds)) # TODO: use time stamps instead of length
    y = speeds

    plt.plot(x, y, '-') 
    plt.show()

    break