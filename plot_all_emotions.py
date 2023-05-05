'''
this code creates a dynamic line plot of emotions or sentiment based on the scores we computed in 'classify.py' 
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functions import *

def line_plot_emotions(avg_labels):
    """
    Plots a line chart for emotion analysis over time
    """
    window = 20
    if 'anger' in avg_labels:
        avg_labels = {em: moving_average(avg_labels[em], window) for em in avg_labels}
    
    xdata = []
    ydata = {em: [] for em in avg_labels.keys()}
    try:
        num_points = len(avg_labels['anger'])
    except KeyError:
        num_points = len(avg_labels['positive_sentiment'])

    fig, ax = plt.subplots()

    ln = []
    for em in ydata:
        x, = ax.plot([], [], '-')
        ln.append(x)

    ax.legend(ydata.keys())
    ax.set_xlim(0, num_points)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Time')
    ax.set_ylabel('Moving Average')
    ax.set_title('Emotions for keyword: chatGPT')

    def init():
        """
        Initializes the line plot animation
        """
        try:
            return tuple(ln)
        except:
            return ln[0], ln[1]

    def update(t):
        """
        Updates the line plot animation for each frame
        """
        if t == 0:
            xdata.clear() 
            for em in ydata:
                ydata[em].clear() 
        xdata.append(t)
        for i, em in enumerate(ydata):
            ydata[em].append(avg_labels[em][t])
            ln[i].set_data(xdata, ydata[em])
        try:
            return tuple(ln)
        except:
            return ln[0], ln[1]

    ani = FuncAnimation(fig, update, frames=range(num_points),
                        init_func=init, blit=True, interval=50, repeat=True)
    plt.show()

# main function
if __name__ == '__main__':
    path = '/Users/christiedjidjev/Library/CloudStorage/OneDrive-Personal/Classes/Twitter Sentiment/'

    avg_labels = readFile(path + 'avg_labels.gzip')

    del avg_labels['positive_sentiment']
    del avg_labels['negative_sentiment']

    line_plot_emotions(avg_labels)
