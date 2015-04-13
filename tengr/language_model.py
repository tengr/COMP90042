from nltk.stem import PorterStemmer
import nltk
import math
import os
import re
from  build_load import load_ii_vsm, get_f_names, load_queries

stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"  
dic = load_ii_vsm()
q_num = load_queries() 
f_names = get_f_names()
N = len(f_names)
doc_d = {}
mu = 1.0

for f_name in f_names:
    #with open(dirname + f_name,'r') as f:
        #doc_d[f_name] = len(f.read().split())
    doc_d[f_name] = os.path.getsize(dirname + f_name)

ranking_file = open('lm_vsm_rankings.txt', 'w')

for each_query in q_num:
    print each_query + "\t" + str(q_num[each_query])
    score = {}
    terms = nltk.word_tokenize(re.sub(r"[\W]", " ", each_query.lower()))    
    for term in terms:
        word = stemmer.stem(term)
        if word in dic:
            nt = len(dic[word])
            for doc, freq in dic[word].iteritems():
#                 tf = math.log(1 + freq)
#                 idf = math.log(1.0 * N / nt)
#                 tfidf = tf * idf
                d = doc_d[doc]
                s = freq / (d + mu) + mu * nt / ((d + mu) * N)
                if doc not in score:
                    score[doc] = s
                else:
                    score[doc] += s
        
    sorted_docs = sorted(score, key=score.get, reverse=True)
    
    for doc in sorted_docs:
        ranking_file.write(str(q_num[each_query]) + " 0 " + doc + " " + str(score[doc]) + "\n" ) 
            
