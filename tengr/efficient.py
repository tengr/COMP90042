import nltk
import sys
import re
import string
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import *
from nltk.corpus import stopwords   
from pip._vendor.requests.packages.chardet.latin1prober import FREQ_CAT_NUM
from cmath import log
import pickle
import cPickle

def process_query_file():
    q = {}
    num = 0
    query = ""
    with open("/Users/ruichen/Documents/COMP90042/proj1/proj1data/06.topics.851-900.txt","r") as query_file:
        for line in query_file:
            if "<num>" in line:
                num = int(line.split()[-1])
            elif "<title>" in line:
                query = line.replace('<title>','').replace('"','').strip()
                q[num] = query
            
    return q

def increment_last_number(s):
    for i in range(len(s)-1, -1, -1):
        if s[i] == ' ':
            return s[0:i+1] + str(int(s[i+1:len(s)]) + 1)
        
def save_word_file():
    cPickle.dump(word_file,open("word_file.dat",'w'), pickle.HIGHEST_PROTOCOL)

def load_word_file():
    return cPickle.load(open("word_file.dat",'r'))

def save_word_freq():
    cPickle.dump(word_freq,open("word_freq.dat",'w'), pickle.HIGHEST_PROTOCOL)

def load_word_freq():
    return cPickle.load(open("word_freq.dat",'r'))

word_file = {}
save_word_file()
word_freq = {}
save_word_freq()
word_list = []
stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"
filenames = [f for f in os.listdir(dirname) if os.path.isfile(dirname + f) and os.path.getsize(dirname + f) > 0 ]
stopset = set(stopwords.words('english'))

for filename in filenames[:200]:
    with open(dirname + filename,'r') as f:
        text = re.sub(r"[\W]", " ", f.read())
        tokens = nltk.word_tokenize(text.lower())
        for token in tokens:
            if token not in stopset:
                word = stemmer.stem(token)
                fn = filename.replace("BLOG06-200602", '')
                if word in word_freq: #seen word
                    if fn in word_file[word]:
                        word_freq = load_word_freq()
                        word_freq[word] = increment_last_number(word_freq[word])
                        save_word_freq()
                    else: #seen word, new file
                        word_file = load_word_file()
                        word_file[word] += ' ' + fn
                        save_word_file()
                        
                        word_freq = load_word_freq()
                        word_freq[word] += ' 1'
                        save_word_freq()
                else: #new word
                    word_list.append(word)
                    word_freq = load_word_freq()
                    word_freq[word] = ' 1'
                    save_word_freq()
                    
                    load_word_file()
                    word_file[word] = ' ' + fn
                    save_word_file()
load_word_file()
print word_file
# print word_freq

# for key,value in dic.iteritems():
#     print key + "\t" + str(value)
#     
word_freq[word]

# testq = "understand retirees representative"
# terms = testq.lower().split()
# score = {}
# N = len(filenames)
# for term in terms:
#     word = stemmer.stem(term)
#     if word in word_list:
#         docs = word_file[word].split()
#         freqs = word_freq[word].split()
#         nt = len(docs) #N documents have the word
#         idf = log(N * 1.0 / nt)
#         index = -1
#         for doc in docs:
#             index += 1
#             freq = int(freqs[index])
#             tfidf = log(freq + 1) * idf
#             if doc not in score:
#                 score[doc] = tfidf
#             else:
#                 score[doc] += tfidf
#    
# for key, value in score.iteritems():
#     print key + "\t" + str(value)
        



    