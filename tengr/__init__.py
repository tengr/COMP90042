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

# def tokenize_corpus(str):
#     return  nltk.word_tokenize(str.strip(string.punctuation))
    #return regexp_tokenize(str, r'[,\.\?!"\s:\xc2\x99]', gaps=True)
    #return str.split(r'[,.:!]')

def read_files(filenames, n):
    for filename in filenames[:n]:
        text = open('/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/'+filename,'r').read()
    #print text
        #re.DOTALL
    text = re.sub(r"[\W]"," ",text)
    return text

# def case_fold(str):
#     return str.lower()

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

dic = {}
stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"
filenames = [f for f in os.listdir(dirname) if os.path.isfile(dirname + f) and os.path.getsize(dirname + f) > 0 ]
stopset = set(stopwords.words('english'))
print "len" + str(len(filenames))

for filename in filenames[:1]:
    with open(dirname + filename,'r') as f:
        text = re.sub(r"[\W]", " ", f.read())
        tokens = nltk.word_tokenize(text.lower())
        for token in tokens:
            if token not in stopset:
                word = stemmer.stem(token.decode('utf8', 'ignore'))
                if word in dic:
                    if filename in dic[word]:
                        dic[word][filename] += 1
                    else:
                        dic[word][filename] = 1
                else: 
                    dic[word] = {}
                    dic[word][filename] = 1

for key,value in dic.iteritems():
    print key + "\t" + str(value)
    
#pickle.dump(dic,open("dic.txt",'w'), pickle.HIGHEST_PROTOCOL)
cPickle.dump(dic,open("dic.dat",'w'), pickle.HIGHEST_PROTOCOL)


# testq = "understand retirees representative"
# terms = testq.lower().split()
# score = {}
# for term in terms:
#     if term in dic:
#         for doc, freq in dic[term].iteritems():
#             N = len(dic[term])
#             idf = 1.0 / log(N)
#             freq = dic[term][doc]
#             tfidf = log(freq + 1) * idf
#             if doc not in score:
#                 score[doc] = tfidf
#             else:
#                 score[doc] += tfidf
#  
# for key, value in score.iteritems():
#     print key + "\t" + str(value)
        



    