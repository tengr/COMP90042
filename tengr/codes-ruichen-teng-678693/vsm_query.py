from nltk.stem import PorterStemmer
import nltk
import math
import re
from  build_load import load_ii_vsm, get_f_names, load_queries

stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"  
dic = load_ii_vsm()
q_num = load_queries() 
f_names = get_f_names()
N = len(f_names)
doc_lensq = {}

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

ranking_file = open('vsm_rankings.txt', 'w')

for each_query in q_num:
    print each_query + "\t" + str(q_num[each_query])
    score = {}
    terms = nltk.word_tokenize(re.sub(r"[\W]", " ", each_query.lower()))    
    for term in terms:
        word = stemmer.stem(term)
        if word in dic:
            nt = len(dic[word])
            for doc, freq in dic[word].iteritems():
                tf = math.log(1 + freq)
                idf = math.log(1.0 * N / nt)
                tfidf = tf * idf
                if doc not in score:
                    score[doc] = tfidf
                else:
                    score[doc] += tfidf
    
    for doc in score:
        score[doc] /= math.sqrt(doc_lensq[doc])
        
    sorted_docs = sorted(score, key=score.get, reverse=True)
    
    for doc in sorted_docs:
        ranking_file.write(str(q_num[each_query]) + " 0 " + doc + " " + str(score[doc]) + "\n" ) 
            
