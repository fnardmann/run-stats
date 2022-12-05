# Track Progress from Interval Running
This is a little script to track and visualize your progress while doing interval training. The neccessary `.fit` files can be exported via services like Garmin Connect. Just collect all your interval workouts in a directory and execute the `main.py` script. To get comparable results the workouts should have similiar properties (e.g. interval length, route, warmup, length). Of course there are some other factors like fatigue or just daily fitness which can influence the tempo of your intervals, but all in all you should be abled to track if you are improving over time or not.  
  
To visualize several intervals of a single session equally a boxplot is used. The red line in the middle of the boxplots corresponds to the median of all given interval paces. The upper and lower bound of the pink boxes correspond to the upper (75th) and lower (25th) quartile oft the given data. For an effictive interval workout your paces for each interval should be somehow equal, in this case the boxes would be relative small indicating a smaller variance.

![result](https://user-images.githubusercontent.com/59708022/205741785-1bf92d77-45e2-4a41-966d-4e7eaf984e50.png)



## TODO
- include heartrate in analysis
- allow other interval lengths
