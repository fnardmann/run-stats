import fitparse
import glob
import matplotlib.pyplot as plt

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


    plt.plot(range(len(speeds)), speeds, '-') 
    plt.show()

    break