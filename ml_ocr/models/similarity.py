"""
Semantic similarity is a metric defined over a set of documents or terms, where the idea of distance between items is
based on the likeness of their meaning or semantic content  Semantic similarity includes “is a” relations. JNBHFor example, “car” is similar to “bus“

estimating the semantic similarity between a pair of sentences is by taking the average of the word embeddings of all
words in the two sentences, and calculating the cosine between the resulting embeddings.
Obviously, this simple baseline leaves considerable room for variation.
We’ll investigate the effects of ignoring stopwords and computing an average weighted by tf-idf in particular.
"""
import math
import string
import sys
import os


# reading the text file
# This function will return a
# list of the lines of text
# in the file.
def read_file(filename):
    try:
        with open(os.path.join('tmp', filename), 'rb') as f:
            data = f.read()
        return data

    except IOError:
        print("Error opening or reading input file: ", filename)
        sys.exit()


# splitting the text lines into words
# translation table is a global variable
# mapping upper case to lower case and
# punctuation to spaces
translation_table = str.maketrans(string.punctuation + string.ascii_uppercase,
                                  " " * len(string.punctuation) + string.ascii_lowercase)


# returns a list of the words
# in the file
def get_words_from_line_list(text):
    text = text.translate(translation_table)
    word_list = text.split()

    return word_list


# counts frequency of each word
# returns a dictionary which maps
# the words to their frequency.
def count_frequency(word_list):
    D = {}

    for new_word in word_list:

        if new_word in D:
            D[new_word] = D[new_word] + 1

        else:
            D[new_word] = 1

    return D


# returns dictionary of (word, frequency)
# pairs from the previous dictionary.
def word_frequencies_for_file(output_data):
    # line_list = read_file(filename)
    word_list = get_words_from_line_list(output_data)
    freq_mapping = count_frequency(word_list)

    # print("File", filename, ":", )
    print(len(output_data), "lines, ", )
    print(len(word_list), "words, ", )
    print(len(freq_mapping), "distinct words")

    return freq_mapping


# returns the dot product of two documents
def dotProduct(D1, D2):
    Sum = 0.0

    for key in D1:

        if key in D2:
            Sum += (D1[key] * D2[key])

    return Sum


# returns the angle in radians
# between document vectors
def vector_angle(D1, D2):
    numerator = dotProduct(D1, D2)
    denominator = math.sqrt(dotProduct(D1, D1) * dotProduct(D2, D2))

    return math.acos(numerator / denominator)


def similarity_ml(output_data_1, output_data_2):
    # filename_1 = sys.argv[1]
    # filename_2 = sys.argv[2]
    sorted_word_list_1 = word_frequencies_for_file(output_data_1)
    sorted_word_list_2 = word_frequencies_for_file(output_data_2)
    distance = vector_angle(sorted_word_list_1, sorted_word_list_2)

    return distance


# Driver code
# documentSimilarity('GFG.txt', 'file.txt')
