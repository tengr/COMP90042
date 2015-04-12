#implementing Rocchio's Relevance Feedback Algorithm
import os
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
import math
import re
import cPickle
from build_load import load_queries, load_ii_vsm, get_f_names
from process_results import get_results

q_num = load_queries()
#print q_num
#print q_num.keys()
f_names = get_f_names()
res = get_results('vsm_rankings.txt')
dic = load_ii_vsm()
alpha = 0.5
beta = 0.5
gama = 0.0
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"
stemmer = PorterStemmer()
stopset = set(stopwords.words('english'))
N = len(f_names)
doc_lensq = {}
#ranking_file = open('rocchio_vsm_rankings.txt', 'w')
doc_len = {}
doc_vec = {}

def get_doc_vec(f_name):
    if f_name not in doc_vec:
        word_weight = {}
        with open(dirname + f_name,'r') as f:
            text = re.sub(r"[\W]", " ", f.read())
            tokens = nltk.word_tokenize(text.lower())
            for token in tokens:
                if token not in stopset:
                    word = stemmer.stem(token.decode('utf8', 'ignore'))
                    #print f_name + "\t" + word
                    if word in dic and word not in word_weight:
                        #print dic['of']  
                        #print f_name + "new word\t" + word
                        nt = len(dic[word])
                        freq = dic[word][f_name]
                        tf = math.log(1 + freq)
                        idf = math.log(1.0 * N / nt)
                        tfidf = tf * idf
                        word_weight[word] = tfidf
        doc_vec[f_name] = Counter(word_weight)
    return doc_vec[f_name] 

def get_doc_len(f_name):
    if f_name not in doc_len:
        weights = dict(get_doc_vec(f_name)).values()
        l = 0.0
        for weight in weights:
            l += weight
        doc_len[f_name] = math.sqrt(l)
    return doc_len[f_name]

def build_num_qe():
    num_qe = {}
    for q in q_num:
        num = q_num[q]
        print q + "\t" + str(num)
        terms = nltk.word_tokenize(re.sub(r"[\W]", " ", q.lower()))           
        q0dic = {}
        for term in terms:
            if term not in stopset:
                word = stemmer.stem(term.decode('utf8', 'ignore'))
                if word in dic:
                    q0dic[word] = alpha
        alphaq0 = Counter(q0dic)
        #Dr = len(res[num]) #number of relevant documents
        #print "Dr = " + str(Dr)
        Dr = 100
        #print "Dr = " + str(Dr)
        sum_docvec = Counter()
        for name in res[num][:Dr]:
            f_name = name + '.txt'
            sum_docvec += get_doc_vec(f_name)
            #print sum_docvec
        #sum_docvecdic = dict(sum_docvec)
        #qe = dict(alphaq0 + Counter(sum_docvecdic.update((k, v * beta / Dr) for k, v in  sum_docvecdic.iteritems())))
        #print sum_docvec.values()[0]
        for k in sum_docvec:
            sum_docvec[k] *= beta/Dr
        #print sum_docvec.values()[0]
        qe = dict(alphaq0 + sum_docvec)
        num_qe[num] = qe
        #print qe.values()[0]
        #break
    cPickle.dump(num_qe, open('num_qe.dat','w',cPickle.HIGHEST_PROTOCOL))

def load_num_qe():
    if not os.path.isfile('num_qe.dat'):
        build_num_qe()
    return cPickle.load(open('num_qe.dat','r'))

def get_qe_len(num):
    weights = num_qe[num].values()
    l = 0.0
    for weight in weights:
        l += weight
    return math.sqrt(l)

def prod_doc_qe(f_name, qenum):
    docvec = dict(get_doc_vec(f_name))
    s = 0.0
    for word in num_qe[qenum]:
        if word in docvec:
            s += num_qe[qenum][word] * docvec[word]
    return s / (get_doc_len(f_name) * get_qe_len(qenum))
#getting the updated query vectors

num_qe = load_num_qe()
#print num_qe

# for num in num_qe:
#     score = {}
#     for word in num_qe[num]:
#         for doc in dic[word]:
#             if doc not in score:
#                 score[doc] = prod_doc_qe(doc, num)
#      
#     sorted_docs = sorted(score, key=score.get, reverse=True)
#      
#     for doc in sorted_docs:
#         ranking_file.write(str(num) + " 0 " + doc + " " + str(score[doc]) + "\n" ) 

for word in dic:
    nt = len(dic[word])
    for doc, freq in dic[word].iteritems():
        tf = math.log(1 + freq)
        idf = math.log(1.0 * N / nt)
        tfidf = tf * idf
        if doc not in doc_lensq:
            doc_lensq[doc] = tfidf ** 2
        else:
            doc_lensq[doc] += tfidf ** 2

ranking_file = open('roch_vsm_rankings.txt', 'w')

for each_query in q_num:
    print each_query + "\t" + str(q_num[each_query])
    num = q_num[each_query]
    qe = num_qe[num]
    score = {}
    for word in num_qe[num]:
        if word in dic:
            nt = len(dic[word])
            for doc, freq in dic[word].iteritems():
                tf = math.log(1 + freq)
                idf = math.log(1.0 * N / nt)
                tfidf = tf * idf
                w = tfidf * qe[word]
                if doc not in score:
                    score[doc] = w
                else:
                    score[doc] += w
    
    for doc in score:
        score[doc] /= math.sqrt(doc_lensq[doc])
        
    sorted_docs = sorted(score, key=score.get, reverse=True)
    
    for doc in sorted_docs:
        ranking_file.write(str(q_num[each_query]) + " 0 " + doc + " " + str(score[doc]) + "\n" ) 
