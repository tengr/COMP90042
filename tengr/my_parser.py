'''
@author: ZZ
'''
import re
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords
import os

# Get filtered words.
# Return | A list of filtered words.
def get_filtered_words(text):
    text = text.lower() 
    text = re.sub(r'[^a-z0-9 ]',' ',text)
    text = text.split()
    return [w for w in text if not w in stopwords.words('english')]

# Stemming.
# Return | A list of stemmed words.
def stemming(text):    
    stemmer = PorterStemmer()
    stemmed_words = []
    for word in text:
        stemmed_words.append(stemmer.stem(word))
    return stemmed_words

# Generate inverted index.
# def generate_inverted_index_for_one_file(text,file_name,inverted_index):
#     for word in text:
#         if not inverted_index.has_key(word):
#             inverted_index[word] = {}
#             inverted_index[word][file_name] = 1
#         else:
#             if not inverted_index[word].has_key(file):
#                 inverted_index[word][file_name] = 1
#             else:
#                 inverted_index[word][file_name] = inverted_index[word][file_name] + 1