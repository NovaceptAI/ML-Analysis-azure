from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.parsing.preprocessing import STOPWORDS


def summarization_ml(output_data):
    # Tokenizing the text
    stopWords = set(STOPWORDS)
    words = word_tokenize(output_data.lower())

    # Creating a frequency table to keep the score of each word
    freqTable = {}
    for word in words:
        if word in stopWords:
            continue
        freqTable[word] = freqTable.get(word, 0) + 1

    # Creating a dictionary to keep the score of each sentence
    sentences = sent_tokenize(output_data)
    sentenceValue = {}

    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freqTable:
                sentenceValue[sentence] = sentenceValue.get(sentence, 0) + freqTable[word]

    # Calculate the average value of a sentence
    average = sum(sentenceValue.values()) / len(sentenceValue) if sentenceValue else 0

    # Generating the summary based on sentence scores
    summary = ' '.join(sentence for sentence, value in sentenceValue.items() if value > 1.2 * average)

    return summary
