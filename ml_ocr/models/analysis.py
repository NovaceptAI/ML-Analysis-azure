# Define Imports
import re
import os
import nltk
import ssl
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

download_dir = os.path.abspath('nltk_data')
# nltk.download('wordnet', download_dir=download_dir)
# nltk.data.load(os.path.join(download_dir, 'tokenizers/punkt/english.pickle'))
# nltk.data.load(os.path.join(download_dir, 'taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle'))
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def lemmatize_stemming(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')


# function to calculate subjectivity
def getSubjectivity(review):
    return TextBlob(review).sentiment.subjectivity

    # function to calculate polarity
    def getPolarity(review):
        return TextBlob(review).sentiment.polarity


# function to analyze the reviews
def analysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def clean(text):
    # Removes all special characters and numerical leaving the alphabets
    text = re.sub('[^A-Za-z]+', ' ', text)
    return text


def sentiment_analysis(text):
    positive_sentences = 0
    negative_sentences = 0
    neutral_sentences = 0
    sentence_sentiment = []
    for single_statement in text:
        single_statement = clean(single_statement.text)
        result = []
        for token in simple_preprocess(single_statement):
            if token not in STOPWORDS and len(token) > 3:
                result.append(lemmatize_stemming(token))

        tokens = word_tokenize(single_statement)
        # pos = nltk.pos_tag(tokens)
        new_text = " ".join(ele for ele in tokens if ele.lower not in STOPWORDS)
        # new_text = " ".join(ele for ele in tokens if ele.lower() not in stopwords.words('english'))
        score = getSubjectivity(new_text)
        sentiment_final = analysis(score)
        if sentiment_final == "Positive":
            positive_sentences += 1
            sentence_sentiment.append({single_statement: "Positive"})
        elif sentiment_final == "Negative":
            negative_sentences += 1
            sentence_sentiment.append({single_statement: "Negative"})
        else:
            neutral_sentences += 1
            sentence_sentiment.append({single_statement: "Neutral"})

    sentiment_final = {"Positive Sentiment": positive_sentences / (len(text)),
                       "Negative Sentiment": negative_sentences / (len(text)),
                       "Neutral Sentiment": neutral_sentences / (len(text)),
                       "All Sentiment": sentence_sentiment}

    return sentiment_final
