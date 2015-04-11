#build and load inverted index for vector space model and positional index
#process query file into a dictionary object
import nltk
import re
import os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords   
import cPickle

stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"
filenames = [f for f in os.listdir(dirname) if os.path.isfile(dirname + f) and os.path.getsize(dirname + f) > 0 ]
stopset = set(stopwords.words('english'))

ii_vsm = 'dic.dat'
ii_pos = 'posdic.dat'

def build_ii_vsm():
    dic = {}
    for filename in filenames:
        with open(dirname + filename,'r') as f:
            text = re.sub(r"[\W]", " ", f.read())
            tokens = nltk.word_tokenize(text.lower())
            for token in tokens:
                if token not in stopset: #comment this line time becomes 5:57
                    word = stemmer.stem(token.decode('utf8', 'ignore'))
                    if word in dic:
                        if filename in dic[word]:
                            dic[word][filename] += 1
                        else:
                            dic[word][filename] = 1
                    else: 
                        dic[word] = {}
                        dic[word][filename] = 1
    cPickle.dump(dic,open(ii_vsm,'w'), cPickle.HIGHEST_PROTOCOL)

def build_ii_pos():
    posdic = {}
    for filename in filenames:
        with open(dirname + filename,'r') as f:
            text = re.sub(r"[\W]", " ", f.read())
            tokens = nltk.word_tokenize(text.lower())
            for i in xrange(len(tokens)):
                word = stemmer.stem(tokens[i].decode('utf8', 'ignore'))
                if word in posdic:
                    if filename in posdic[word]:
                        posdic[word][filename].append(i)
                    else:
                        posdic[word][filename] = [i]
                else: 
                    posdic[word] = {}
                    posdic[word][filename] = [i]
    cPickle.dump(posdic,open(ii_pos,'w'), cPickle.HIGHEST_PROTOCOL)
        
def load_ii_vsm():
    if not os.path.isfile(ii_vsm):
        build_ii_vsm()
    return cPickle.load(open(ii_vsm,'r'))

def load_ii_pos():
    if not os.path.isfile(ii_vsm):
        build_ii_pos()
    return cPickle.load(open(ii_pos,'r'))

def load_queries():
    q_num = {}
    num = 0
    with open("/Users/ruichen/Documents/COMP90042/proj1/proj1data/06.topics.851-900.txt","r") as query_file:
        for line in query_file:
            if "<num>" in line:
                num = int(line.split()[-1])
            elif "<title>" in line:
                query = line.replace('<title>','').replace('"','').strip()
                q_num[query] = num
    return q_num