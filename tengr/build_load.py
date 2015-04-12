#build and load inverted index for vector space model and positional index
#process query file into a dictionary object
import nltk
import re
import os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import cPickle
from collections import Counter
import time

stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"
f_names = [f for f in os.listdir(dirname) if os.path.isfile(dirname + f) and os.path.getsize(dirname + f) > 0 ]
stopset = set(stopwords.words('english'))

ii_vsm = 'vsmdic.dat'
ii_pos = 'posdic.dat'
ii_bi = 'bidic.dat'

def get_f_names():
    return f_names
    
def build_ii_vsm():
    dic = {}
    for f_name in f_names:
        with open(dirname + f_name,'r') as f:
            text = re.sub(r"[\W]", " ", f.read())
            tokens = nltk.word_tokenize(text.lower())
            for token in tokens:
                if token not in stopset: #comment this line time becomes 5:57
                    word = stemmer.stem(token.decode('utf8', 'ignore'))
                    if word in dic:
                        if f_name in dic[word]:
                            dic[word][f_name] += 1
                        else:
                            dic[word][f_name] = 1
                    else: 
                        dic[word] = {}
                        dic[word][f_name] = 1
    cPickle.dump(dic,open(ii_vsm,'w'), cPickle.HIGHEST_PROTOCOL)
    
def build_ii_vsm_fast():
    word_tf = {}
    word_fid = {}
    for f_name in f_names:
        with open(dirname + f_name,'r') as f:
            text = re.sub(r"[\W]", " ", f.read())
            tokens = nltk.word_tokenize(text.lower())
            fid = f_names.index(f_name)
            for token in tokens:
                if token not in stopset: #comment this line time becomes 5:57
                    word = stemmer.stem(token.decode('utf8', 'ignore'))
                    if word in word_tf:
                        if fid in word_fid[word]:
                            word_tf[word][-1] += 1
                        else:
                            word_tf[word].append(1)
                            word_fid[word].append(fid) 
                    else: 
                        word_tf[word] = [1]
                        word_fid[word] = [fid]
    cPickle.dump(word_fid,open("word_fid.dat",'w'), cPickle.HIGHEST_PROTOCOL)
    cPickle.dump(word_tf,open("word_tf.dat",'w'), cPickle.HIGHEST_PROTOCOL)


def build_ii_pos():
    posdic = {}
    for f_name in f_names:
        with open(dirname + f_name,'r') as f:
            text = re.sub(r"[\W]", " ", f.read())
            tokens = nltk.word_tokenize(text.lower())
            file_id = f_names.index(f_name)
            for pos in xrange(len(tokens)):
                word = stemmer.stem(tokens[pos].decode('utf8', 'ignore'))
                if word in posdic:
                    if file_id in posdic[word]:
                        posdic[word][file_id].append(pos)
                    else:
                        posdic[word][file_id] = [pos]
                else: 
                    posdic[word] = {}
                    posdic[word][file_id] = [pos]
    cPickle.dump(posdic,open(ii_pos,'w'), cPickle.HIGHEST_PROTOCOL)
    
def build_ii_bi():
    bidic = {}
    for f_name in f_names:
        with open(dirname + f_name,'r') as f:
            text = re.sub(r"[\W]", " ", f.read())
            tokens = nltk.word_tokenize(text.lower())
            if (len(tokens) > 1): #ignore files with only one word in it
                file_id = f_names.index(f_name)
                word1 = stemmer.stem(tokens[0].decode('utf8', 'ignore'))
                for pos in xrange(1, len(tokens)):
                    word2 = stemmer.stem(tokens[pos].decode('utf8', 'ignore'))
                    word = word1 + ' ' + word2
                    word1 = word2
                    if word in bidic:
                        bidic[word].add(file_id)
                    else: 
                        bidic[word] = set([file_id])
    cPickle.dump(bidic,open(ii_bi,'w'), cPickle.HIGHEST_PROTOCOL)
        
def load_ii_vsm():
    if not os.path.isfile(ii_vsm):
        build_ii_vsm()
    return cPickle.load(open(ii_vsm,'r'))

def load_ii_pos():
    if not os.path.isfile(ii_pos):
        build_ii_pos()
    return cPickle.load(open(ii_pos,'r'))

def load_ii_bi():
    if not os.path.isfile(ii_bi):
        build_ii_bi()
    return cPickle.load(open(ii_bi,'r')) 

def load_queries():
    q_num = {}
    with open("/Users/ruichen/Documents/COMP90042/proj1/proj1data/06.topics.851-900.txt","r") as query_file:
        for line in query_file:
            if "<num>" in line:
                num = int(line.split()[-1])
            elif "<title>" in line:
                query = line.replace('<title>','').replace('"','').strip()
                q_num[query] = num
    return q_num

def check_queries():
    q_num = load_queries()
    len_list = []
    for q in q_num:
        len_list.append(len(q.split()))
    return Counter(len_list)

def time_it(some_method):
    start_time = time.time()
    some_method()
    return time.time() - start_time
#print("--- %s seconds ---" %  time_it((build__ii_vsm)))