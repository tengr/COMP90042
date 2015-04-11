import nltk
import re
from nltk.stem import PorterStemmer
from collections import OrderedDict
from build_load import load_queries, get_f_names, load_ii_bi

# q_num = load_queries()
# id_f_names = map_file_ids()
# posdic = load_ii_pos()
# stemmer = PorterStemmer()

# for each_query in q_num:
#     print each_query + "\t" + str(q_num[each_query])
#     terms = re.sub(r"[\W]", " ", each_query).lower().split()
#     if len(terms > 2): #exclude single-word and bi-word queries 
#         subdic = {} #grab the posting lists needed
#         word_df = {} #see the word with highest df
#         words = [] #stemmed query
#         for term in terms:
#             word = stemmer.stem(term)
#             if word in posdic:
#                 subdic[word] = posdic[word]
#                 word_df[word] = len(posdic[word])
#                 words.append(word)

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
                

                
        
# 
# with open('/Users/ruichen/Documents/COMP90042/proj1/proj1data/qrels.february','r') as f1:
#     for line in f1:
#         arr = line.split()
#         query_num = arr[0]
#         relevance = int(arr[-1])
#         f_name = arr[2]
#         if relevance >= 1:
#             if query_num in ans:
#                 ans[query_num].append(f_name)
#             else:
#                 ans[query_num] = [f_name]
# 
# 
# 
# with open('/Users/ruichen/Documents/workspace/IR/tengr/rankings.txt', 'r') as f2:
#     for line in f2:
#         arr = line.split()
#         query_num = arr[0]
#         f_name = arr[2].replace(".txt", "")
#         if query_num in res:
#             res[query_num].append(f_name)
#         else:
#             res[query_num] = [f_name]

# pre_arr = [] 
# rec_arr = []           
# for i in xrange(10,50):
#     pre_arr.append(precision_at(i, ''))
#     rec_arr.append(recall_at(i, ''))
# plt.plot(pre_arr, rec_arr, 'ro')
# plt.show()
# precision_at(20,'print')

