'''
this code creates a bipartie graph showing the relationship between emotions and sentiment 
based on the frequency of emotion-sentiment pairs in the same tweet. 
'''
import networkx as nx
import matplotlib.pyplot as plt
from functions import *

def biPartite():
    path = '/Users/christiedjidjev/Library/CloudStorage/OneDrive-Personal/Classes/Twitter Sentiment/'
    avg_labels = readFile(path + 'avg_labels.gzip')

    # Define mappings and initialize dictionary
    best_method = {'anger': 'SVCmodel', 'anticipation': 'SVCmodel', 'fear': 'BernoulliNB', 'joy': 'SVCmodel',
                'love': 'SVCmodel', 'optimism': 'log_regression', 'pessimism': 'BernoulliNB'}
    emotions = list(best_method.keys())
    sentiment_emotion_counts = {}

    # Iterate over data to populate dictionary
    for i in range(len(avg_labels['anger'])):
        if avg_labels['positive_sentiment'][i] > 0:
            sent = 'positive_sentiment'
            for em in emotions:
                if avg_labels[em][i] != 0:
                    if (sent, em) not in sentiment_emotion_counts:
                        sentiment_emotion_counts[(sent, em)] = 0
                    sentiment_emotion_counts[(sent, em)] += avg_labels['positive_sentiment'][i]

        if avg_labels['negative_sentiment'][i] < 0:
            sent = 'negative_sentiment'
            for em in emotions:
                if avg_labels[em][i] != 0:
                    if (sent, em) not in sentiment_emotion_counts:
                        sentiment_emotion_counts[(sent, em)] = 0
                    sentiment_emotion_counts[(sent, em)] -= avg_labels['negative_sentiment'][i]

    # Create bipartite graph
    G = nx.Graph()
    sentiments = set([pair[0] for pair in sentiment_emotion_counts.keys()])
    emotions = set([pair[1] for pair in sentiment_emotion_counts.keys()])

    G.add_nodes_from(sentiments, bipartite=0)
    G.add_nodes_from(emotions, bipartite=1)
    for pair, count in sentiment_emotion_counts.items():
        sentiment, emotion = pair
        G.add_edge(sentiment, emotion, weight=count)

    # Draw graph
    pos = {sentiment: (2+3*i, 2) for i, sentiment in enumerate(sentiments)}
    pos.update({emotion: (i, 1) for i, emotion in enumerate(emotions)})

    nx.draw_networkx_nodes(G, pos, node_size=2800, node_color='lightgreen', edgecolors='k')
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, width=[d['weight']/2 for (u, v, d) in G.edges(data=True)])

    plt.axis('off')
    plt.gcf().set_size_inches(12, 5.6)
    plt.show()


# main function
if __name__ == '__main__':
    biPartite()