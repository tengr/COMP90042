from nltk.stem import PorterStemmer
import os
import cPickle
from tengr.io import *
from tengr import io
#global variables
# ans = {} 
# res = {}
# posdic = {}
# q_num = {}

def load_posdic():
    return cPickle.load(open("posdic.dat",'r'))

io()

#posdic = load_posdic()

# print len(posdic)
print "test"
# stemmer = PorterStemmer()
# dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"   
# filenames = [f for f in os.listdir(dirname) if os.path.isfile(dirname + f) and os.path.getsize(dirname + f) > 0 ]




# for each_query in q_num:
#     #print each_query + "\t" + str(q_num[each_query])
#     terms = re.sub(r"[\W]", " ", each_query).lower().strip().split()
#     print posdic    
#     if len(terms > 0):
#         subdic = {}
#         word_df = {}
#         words = []
#         for term in terms:
#             word = stemmer.stem(term)
#             if word in posdic:
#                 subdic[word] = posdic[word]
#                 word_df[word] = len(posdic[word])
#                 words.append(word)
#             else:
#                 break
#     if len(words) == len(terms):
        
# 
# with open('/Users/ruichen/Documents/COMP90042/proj1/proj1data/qrels.february','r') as f1:
#     for line in f1:
#         arr = line.split()
#         query_num = arr[0]
#         relevance = int(arr[-1])
#         filename = arr[2]
#         if relevance >= 1:
#             if query_num in ans:
#                 ans[query_num].append(filename)
#             else:
#                 ans[query_num] = [filename]
# 
# 
# 
# with open('/Users/ruichen/Documents/workspace/IR/tengr/rankings.txt', 'r') as f2:
#     for line in f2:
#         arr = line.split()
#         query_num = arr[0]
#         filename = arr[2].replace(".txt", "")
#         if query_num in res:
#             res[query_num].append(filename)
#         else:
#             res[query_num] = [filename]

# pre_arr = [] 
# rec_arr = []           
# for i in xrange(10,50):
#     pre_arr.append(precision_at(i, ''))
#     rec_arr.append(recall_at(i, ''))
# plt.plot(pre_arr, rec_arr, 'ro')
# plt.show()
# precision_at(20,'print')

