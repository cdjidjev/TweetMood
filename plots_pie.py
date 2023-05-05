'''
this code creates a dynamic pie chart of emotions based on the scores we computed in 'classify.py' 
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functions import *

    
def plots_pie():
    path = '/Users/christiedjidjev/Library/CloudStorage/OneDrive-Personal/Classes/Twitter Sentiment/'
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'limegreen', 'red', 'blue', 'navy', 'magenta', 'crimson']
    num_points = 1000
    window = 10
    num_lists = 7

# Set the percentage of each pie slice that will be "exploded" from the rest of the chart
    explode = [0.01 for _ in range(num_lists)]

# Label each slice of the pie chart with a number
    labels = [str(i) for i in range(num_lists)]

# Initialize a list of counts for each slice
    nums = [0 for _ in range(num_lists)]

# Read in the data from a gzipped pickle file
    avg_labels = readFile(path + 'avg_labels.gzip')

# Compute a moving average for each set of data
    l = [moving_average(avg_labels[key], window) for key in avg_labels]

# Create a new figure and axis object for the pie chart
    fig, ax = plt.subplots()

    def update(num):
        """
    Updates pie chart with new data for each tweet batch and displays it.
    Parameters
    ----------
    num : int
        The number of the tweet batch, indicating which set of data to display.
    """
        ax.clear()
        ax.axis('equal')
        str_num = str(num)
        for i in range(num_lists):
            nums[i] = l[i][num]
        ax.pie(nums, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.set_title('Pie chart for keyword chatGPT \n tweet batch ' + str_num)
        ax.legend(avg_labels.keys())

# Create an animation of the pie chart, updating it for each tweet batch
    ani = FuncAnimation(fig, update, frames=range(100), repeat=True, interval=100)

# Display the pie chart
    plt.show()

# main function
if __name__ == '__main__': 
    plots_pie()

