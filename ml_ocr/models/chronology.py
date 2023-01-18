# # -*- coding: utf-8 -*-
# import spacy
# import nltk
# from nltk.tag import StanfordNERTagger
# from nltk.tokenize import word_tokenize
# from nltk.metrics.scores import accuracy
# import os
# java_path = "/home/novneetpatnaik/Downloads/usr/java/jre1.8.0_321/bin/"
# os.environ['JAVAHOME'] = java_path
# # from spacy import displacy
# #
# # nlp = spacy.load('en')
# st = StanfordNERTagger('/all.3class.distsim.crf.ser.gz',
#                        '/stanford-ner.jar',
#                        encoding='utf-8')
#
#
def chronology_ml(raw_annotations):
    return "None"
#     tokenized_text = word_tokenize(raw_annotations)
#     classified_text = st.tag(tokenized_text)
#
#     print(classified_text)
#     split_annotations = classified_text.split()
#     # Amend class annotations to reflect Stanford's NERTagger
#     for n, i in enumerate(split_annotations):
#         if i == "I-PER":
#             split_annotations[n] = "DATE"
#         if i == "I-ORG":
#             split_annotations[n] = "ORGANIZATION"
#         if i == "I-LOC":
#             split_annotations[n] = "LOCATION"
#
#     # Group NE data into tuples
#     def group(lst, n):
#         for i in range(0, len(lst), n):
#             val = lst[i:i + n]
#             if len(val) == n:
#                 yield tuple(val)
#
#     reference_annotations = list(group(split_annotations, 2))
