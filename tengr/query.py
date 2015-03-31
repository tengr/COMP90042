import cPickle
import os
from nltk.stem import PorterStemmer
import math

q_num = {}
num = 0
with open("/Users/ruichen/Documents/COMP90042/proj1/proj1data/06.topics.851-900.txt","r") as query_file:
    for line in query_file:
        if "<num>" in line:
            num = int(line.split()[-1])
        elif "<title>" in line:
            query = line.replace('<title>','').replace('"','').strip()
            q_num[query] = num
        
dic = cPickle.load(open("dic.dat",'r'))
stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"   
filenames = [f for f in os.listdir(dirname) if os.path.isfile(dirname + f) and os.path.getsize(dirname + f) > 0 ]
N = len(filenames)
doc_len = {}


for word in dic:
    nt = len(dic[word])
    for doc, freq in dic[word].iteritems():
        idf = math.log(N * 1.0 / nt)
        tfidf = math.log(freq + 1) * idf
        if doc not in doc_len:
            doc_len[doc] = tfidf ** 2
        else:
            doc_len[doc] += tfidf ** 2

ranking_file = open('rankings.txt', 'w')


for each_query in q_num:
    print each_query + "\t" + str(q_num[each_query])
    score = {}
    terms = each_query.lower().split()
    
    for term in terms:
        word = stemmer.stem(term)
        if word in dic:
            nt = len(dic[word])
            for doc, freq in dic[word].iteritems():
                idf = math.log(N * 1.0 / nt)
                tfidf = math.log(freq + 1) * idf
                if doc not in score:
                    score[doc] = tfidf
                else:
                    score[doc] += tfidf
    
    for doc in score:
        score[doc] /= math.sqrt(doc_len[doc])
        
    sorted_docs = sorted(score, key=score.get, reverse=True)
    
    for doc in sorted_docs:
        ranking_file.write(str(q_num[each_query]) + " 0 " + doc + " " + str(score[doc]) + "\n" ) 
            
