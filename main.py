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