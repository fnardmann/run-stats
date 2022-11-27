import fitparse
import glob
import matplotlib.pyplot as plt
import numpy as np

files = glob.glob("activities/*.fit")

for file in files:

    # Load the FIT file
    fitfile = fitparse.FitFile(file)

    speeds = []

    # Iterate over all messages of type "record"
    # (other types include "device_info", "file_creator", "event", etc)
    for record in fitfile.get_messages("record"):

        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in record:

            if data.name == "enhanced_speed":
                speeds.append(data.value)


    speeds = np.array(speeds)
    # cut off very slow entries at the start
    speeds = speeds[speeds > 1.0]
    
    # speed values are stored in m/s
    speeds = speeds * 60 * 60 / 1000 # km/h
    speeds = 3600 / speeds / 60 # min/km

    plt.gca().invert_yaxis()

    plt.plot(range(len(speeds)), speeds, '-') 
    plt.show()

    break