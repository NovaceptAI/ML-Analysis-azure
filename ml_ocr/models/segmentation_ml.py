# import spacy library
import spacy
# import en_core_web_sm
# from nltk.corpus import wordnet


def segmentation_ml(output_data):
    # load core english library
    nlp = spacy.load("en_core_web_sm")
    # nlp = en_core_web_sm.load()
    # take unicode string
    # here u stands for unicode
    doc = nlp(output_data)
    # to print sentences
    print_list = []
    for sent in doc.sents:
        print_list.append(sent)

    return print_list
