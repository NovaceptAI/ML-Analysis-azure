from gensim import models, utils, parsing, corpora
# from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from .analysis import lemmatize_stemming

# stop = set(stopwords.words('english'))
lemma = WordNetLemmatizer()


# Receive Segmented Data and preprocess the data
def preprocess(text):
    result = []
    for text_value in text:
        for token in utils.simple_preprocess(text_value):
            if token not in parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(lemmatize_stemming(token))
    return result


def tf_idf(bow_corpus):
    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    return corpus_tfidf


def process_docs(text):
    # return "No Data", "No Data"
    # Store the segmented text
    text_list = []
    for i in range(len(text)):
        for text_value in text[i].sents:
            text_list.append(text_value.text)
    processed_docs = preprocess(text_list)
    res = [sub.split() for sub in processed_docs]
    dictionary = corpora.Dictionary(res)
    count = 0
    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in res]

    corpus_tfidf = tf_idf(bow_corpus)

    try:
        lda_model = models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)
        # for idx, topic in lda_model.print_topics(-1):
        #     print('Topic: {} \nWords: {}'.format(idx, topic))
        lda_model_list = []
        lda_model_tfidf = models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)
        for idx, topic in lda_model_tfidf.print_topics(-1):
            # print('Topic: {} Word: {}'.format(idx, topic))
            lda_model_list.append(str(idx))
            lda_model_list.append(topic)

        model_dict = lda_model.id2word
        analysis_list = []
        for i in model_dict.values():
            analysis_list.append(i)
        analysis_text = ' '.join([str(elem) for elem in analysis_list])

        return lda_model_list, analysis_text

    except:
        return "Topic Modelling was not possible on this document", "Could not be identified"

