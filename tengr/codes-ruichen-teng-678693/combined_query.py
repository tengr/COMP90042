from nltk.stem import PorterStemmer
import nltk
import math
import re
from collections import OrderedDict
from  build_load import load_ii_vsm, load_ii_pos, get_f_names, load_queries

stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"  
dic = load_ii_vsm()
posdic = load_ii_pos()
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
            
doc_pivotedn = {}
pivot = 13.36
slope = 0.75
for doc in doc_lensq:
    old_n = math.sqrt(doc_lensq[doc])
    pivoted_n = (1.0 - slope) * pivot + slope * old_n
    doc_pivotedn[doc] = pivoted_n

ranking_file = open('combined_rankings.txt', 'w')

for each_query in q_num:
    print each_query + "\t" + str(q_num[each_query])
    terms = nltk.word_tokenize(re.sub(r"[\W]", " ", each_query.lower()))
    if len(terms) == 1: #single word query
        score = {}
        word = stemmer.stem(terms[0])
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
            score[doc] /= pivoted_n
        sorted_docs = sorted(score, key=score.get, reverse=True)
        for doc in sorted_docs:
            ranking_file.write(str(q_num[each_query]) + " 0 " + doc + " " + str(score[doc]) + "\n" ) 
    else:
        subdic = {} #grabing subdictionary
        words = []
        for i in xrange(len(terms)):
                word = stemmer.stem(terms[i].decode('utf8', 'ignore'))
                if word in posdic:
                    subdic[word] = posdic[word]
                    words.append(word)
                else:
                    subdic = {}
                    words = []
                    break
        if len(subdic) > 0:
            #order by total number of items (possible positions) in the sub dictionary
            #print subdic
            ordered_subdic = OrderedDict(sorted(subdic.items(), key=lambda t: -sum(len(v) for v in t[1].itervalues())))
            popeditem = ordered_subdic.popitem()
            lstfreterm = popeditem[0] #start from the least frequent term, thus search the least number of positions
            lstfreterm_pos = popeditem[1] #this is a dictionary
            #print lstfreterm_pos
            lstfreterm_i = words.index(lstfreterm) #this method finds the first occurance of the term
            #ordered_subdic = OrderedDict(sorted(subdic.items(), key=lambda t: -sum(len(v) for v in t[1].itervalues())))
            #do this again in case duplicate terms in the query, dictionary entry should be deleted in this case
            doc_positions = lstfreterm_pos.copy() #make a copy
            #for w in ordered_subdic:
                #if w_i != lstfreterm_i: #not the least frequent term
                    #w = words[w_i]
            while len(ordered_subdic) > 0:
                popeditem = ordered_subdic.popitem()
                nextterm = popeditem[0]
                nextterm_pos = popeditem[1]
                nextterm_i = words.index(nextterm)
                posdiff = nextterm_i - lstfreterm_i
                for doc_id in lstfreterm_pos:
                    if doc_id in nextterm_pos:
                        doc_positions[doc_id] = list(set(lstfreterm_pos[doc_id]).intersection(set(map(lambda x:x-posdiff,nextterm_pos[doc_id]))))
                        if len(doc_positions[doc_id]) == 0:
                            doc_positions.pop(doc_id)
                    elif doc_id in doc_positions:#there are query words not in this document, won't be considered anymore
                        doc_positions.pop(doc_id)
            lstfreterm_pos = doc_positions.copy()
            
            ordered_doc_positions = OrderedDict(sorted(doc_positions.items(), key=lambda t: -len(t[1])))          
            for doc_id in ordered_doc_positions:
                if len(ordered_doc_positions[doc_id]) > 0:
                    #print doc_id
                    ranking_file.write(str(q_num[each_query]) + " 0 " + f_names[doc_id] + " " + "1\n" )           
