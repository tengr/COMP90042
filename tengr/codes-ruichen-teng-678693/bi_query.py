import nltk
import re
from nltk.stem import PorterStemmer
from collections import OrderedDict
from build_load import load_queries, get_f_names, load_ii_bi

bi_ranking_file = open('bi_rankings.txt', 'w')
q_num = load_queries()
f_names = get_f_names()
bidic = load_ii_bi()
stemmer = PorterStemmer()
for each_query in q_num:
    #print each_query + "\t" + str(q_num[each_query])
    terms = nltk.word_tokenize(re.sub(r"[\W]", " ", each_query.lower()))
    if len(terms) > 1:
        word1 = stemmer.stem(terms[0].decode('utf8', 'ignore'))
        subdic = {} #grabing subdictionary
        for i in xrange(1, len(terms)):
                word2 = stemmer.stem(terms[i].decode('utf8', 'ignore'))
                word = word1 + ' ' + word2
                word1 = word2
                if word in bidic:
                    subdic[word] = bidic[word]
                else:
                    subdic = {}
                    break
        if len(subdic) > 0:
            ordered_subdic = OrderedDict(sorted(subdic.items(), key=lambda t: -len(t[1])))
            doc_ids = ordered_subdic.popitem()[1]
            while len(ordered_subdic) > 0:
                doc_ids = doc_ids.intersection(ordered_subdic.popitem()[1])
            for doc_id in doc_ids:
                bi_ranking_file.write(str(q_num[each_query]) + " 0 " + f_names[doc_id] + " " + "1\n" )
                

                


