# Track Progress from Interval Running
This is a little script to track and visualize your progress while doing interval training. The neccessary `.fit` files can be exported via services like [Garmin Connect](https://connect.garmin.com/modern/). Just collect all your interval workouts in a directory and execute the `main.py` script. To get comparable results the workouts should have similiar properties (e.g. interval length, route, warmup, length). Of course there are some other factors like fatigue or just daily fitness which can influence the tempo of your intervals, but all in all you should be abled to track if you are improving over time or not.  
  
To visualize several intervals of a single session equally a boxplot is used. The red line in the middle of the boxplots corresponds to the median of all given interval paces. The upper and lower bound of the pink boxes correspond to the upper (75th) and lower (25th) quartile oft the given data. For an effictive interval workout your paces for each interval should be somehow equal, in this case the boxes would be relative small indicating a smaller variance.  
  
This uses the very good library [fitparse](https://github.com/dtcooper/python-fitparse) to parse and extract information from the `.fit` files.

## Steps to reproduce
1. Create `conda` environment with:
```
conda create --name <env> --file requirements.txt
```
2. Download original data from [Garmin Connect](https://connect.garmin.com/modern/)
3. Unzip all files with:
```
unzip \*.zip
```
4. Replace activities with your own
5. Run `python main.py` to execute script

## Result Plot

![result](https://user-images.githubusercontent.com/59708022/209859399-c0ca1028-f49d-4e48-a122-20eae4df3d6f.png)
