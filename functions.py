import gzip
import pickle
import re

def readFile(fileName):
    """
    Reads a gzip file and returns its content using pickle
    """
    with gzip.GzipFile(fileName, 'rb') as f:
        return pickle.load(f)
    
def writeFile(fileName, d):    
    """
    Writes a file under filename and returns its content using pickle
    """
    with gzip.GzipFile(fileName, 'wb') as fp:
        pickle.dump(d,fp)  

stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
             'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
             'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
             'does', 'doing', 'down', 'during', 'each','few', 'for', 'from',
             'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
             'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
             'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
             'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
             'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
             't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
             'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
             'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
             'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
             'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
             "youve", 'your', 'yours', 'yourself', 'yourselves', 'but', 'ð', 'like']

def preprocess(dataset):
    #Making statement text in lowercase
    dataset['Tweet']=dataset['Tweet'].str.lower()
    #region Cleaning and removing the above stop words list from the tweet text
    STOPWORDS = set(stopwordlist)
    def cleaning_stopwords(text):
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])
    dataset['Tweet'] = dataset['Tweet'].apply(lambda text: cleaning_stopwords(text))

    #Cleaning and removing punctuations
    import string
    english_punctuations = string.punctuation
    punctuations_list = english_punctuations
    def cleaning_punctuations(text):
        translator = str.maketrans('', '', punctuations_list)
        return text.translate(translator)
    dataset['Tweet']= dataset['Tweet'].apply(lambda x: cleaning_punctuations(x))

    #Cleaning and removing repeating characters
    def cleaning_repeating_char(text):
        return re.sub(r'(.)1+', r'1', text)
    dataset['Tweet'] = dataset['Tweet'].apply(lambda x: cleaning_repeating_char(x))

    #Cleaning and removing URLs
    def cleaning_URLs(data):
        return re.sub('((www.[^s]+)|(https?://[^s]+))',' ',data)
    dataset['Tweet'] = dataset['Tweet'].apply(lambda x: cleaning_URLs(x))

    #Cleaning and removing numbers
    def cleaning_numbers(data):
        return re.sub('[0-9]+', '', data)
    dataset['Tweet'] = dataset['Tweet'].apply(lambda x: cleaning_numbers(x))

    #Getting tokenization of tweet text
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    dataset['Tweet'] = dataset['Tweet'].apply(tokenizer.tokenize)

    return dataset
    #endregion

def moving_average(l, window_size):
    """
    Computes a moving average of a list of values.

    Parameters
    ----------
    l : list
        List of values to compute moving average for.
    window_size : int
        Size of the window to compute the moving average over.

    Returns
    -------
    moving_avg : list
        List of the computed moving averages, where the ith value in the list is
        the average of the ith to the ith + window_size values in the input list.
    """
    cumsum = [0] + list(np.cumsum(l))
    return [(cumsum[i + window_size] - cumsum[i]) / window_size for i in range(len(l) - window_size + 1)]