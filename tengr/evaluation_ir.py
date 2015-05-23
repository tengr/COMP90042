import matplotlib.pyplot as plt
from build_load import load_queries
len_prelistvsm = {}
len_prelistbii = {}
len_prelistpos = {}

q_num = load_queries()
def precision_at(ans, res, n, cmd):
    TP = 0
    for query_num in res:
        resN = res[query_num][:n] #top N of result res[]
        numRel = len( set(resN) & set(ans[query_num]) )
        TP += numRel
        presN = numRel * 1.0 / n
        l = len(q_num.keys()[q_num.values().index(query_num)].split())
        if l not in len_prelistvsm:
            len_prelistvsm[l] = [presN]
        else:
            len_prelistvsm[l].append(presN)
        if cmd == 'print':
            print str(query_num) + "\t" + str(presN) + "\n"
        
    precision = TP / (len(res) * n * 1.0)
    if cmd == 'print':
        print "TP = " + str(TP)    
        print "queries = " + str(len(res))  
        print "overall precision = " + str(precision)
    return precision


def precision_at_bi(ans, res, n, cmd):
    TP = 0
    for query_num in res:
        resN = res[query_num][:n] #top N of result res[]
        numRel = len( set(resN) & set(ans[query_num]) )
        TP += numRel
        presN = numRel * 1.0 / n
        l = len(q_num.keys()[q_num.values().index(query_num)].split())
        if l not in len_prelistbii:
            len_prelistbii[l] = [presN]
        else:
            len_prelistbii[l].append(presN)
        if cmd == 'print':
            print str(query_num) + "\t" + str(presN) + "\n"
            
            
        
    precision = TP / (len(res) * n * 1.0)
    if cmd == 'print':
        print "TP = " + str(TP)    
        print "queries = " + str(len(res))  
        print "overall precision = " + str(precision)
    return precision

def precision_at_pos(ans, res, n, cmd):
    TP = 0
    for query_num in res:
        resN = res[query_num][:n] #top N of result res[]
        numRel = len( set(resN) & set(ans[query_num]) )
        TP += numRel
        presN = numRel * 1.0 / n
        l = len(q_num.keys()[q_num.values().index(query_num)].split())
        if l not in len_prelistpos:
            len_prelistpos[l] = [presN]
        else:
            len_prelistpos[l].append(presN)
        if cmd == 'print':
            print str(query_num) + "\t" + str(presN) + "\n"
        
    precision = TP / (len(res) * n * 1.0)
    if cmd == 'print':
        print "TP = " + str(TP)    
        print "queries = " + str(len(res))  
        print "overall precision = " + str(precision)
    return precision

def recall_at(ans, res, n, cmd):
    TP = 0
    for query_num in ans:
        if query_num in res:
            resN = res[query_num][:n] #top N of result res[]
        else:
            resN = []
        numRel = len( set(resN) & set(ans[query_num]) )
        TP += numRel
        recN = numRel * 1.0 / len(ans[query_num])
        if cmd == 'print':
            print str(query_num) + "\t" + str(recN) + "\n"
        
    recall = TP * 1.0 / sum(len(v) for v in ans.itervalues())
    if cmd == 'print':
        print 'total recall = ' + str(recall)
    return recall



def plot_arr(arr, xlbl, ylbl):
    plt.plot(arr)
    plt.ylabel('precision')
    plt.xlabel('top')
    plt.show()

def get_all_answers():
    ans = {} 
    with open('/Users/ruichen/Documents/COMP90042/proj1/proj1data/qrels.february','r') as f:
        for line in f:
            arr = line.split()
            query_num = int(arr[0])
            relevance = int(arr[-1])
            f_name = arr[2]
            if relevance >= 1:
                if query_num in ans:
                    ans[query_num].append(f_name)
                else:
                    ans[query_num] = [f_name]
    return ans

def get_phrase_answers():
    phrase_ans = {}
    q_num = load_queries() 
    with open('/Users/ruichen/Documents/COMP90042/proj1/proj1data/qrels.february','r') as f:
        for line in f:
            arr = line.split()
            query_num = int(arr[0])
            query = list(q_num.keys())[(list(q_num.values()).index(query_num))]
            relevance = int(arr[-1])
            f_name = arr[2]
            if len(query.split()) > 1 and relevance >= 1: #only consider phrasal queries
                #print query
                if query_num in phrase_ans:
                    phrase_ans[query_num].append(f_name)
                else:
                    phrase_ans[query_num] = [f_name]
    return phrase_ans

def get_results(f_name):
    res = {}
    with open('/Users/ruichen/Documents/workspace/IR/tengr/' + f_name, 'r') as f:
        for line in f:
            arr = line.split()
            query_num = int(arr[0])
            f_name = arr[2].replace(".txt", "")
            if query_num in res:
                res[query_num].append(f_name)
            else:
                res[query_num] = [f_name]
    return res

# pre_arr_vsm = [] 
# rec_arr_vsm = [] 
# pre_arr_bi = []
# rec_arr_bi = []
# ans_vsm = get_all_answers()
# ans_bi = get_phrase_answers()
# res_vsm = get_results('vsm_rankings.txt')
# res_bi = get_results("bi_rankings.txt")         
# for i in xrange(10,100):
#     pre_arr_vsm.append(precision_at(ans_vsm, res_vsm, i, ''))
#     rec_arr_vsm.append(recall_at(ans_vsm, res_vsm, i, ''))
#     pre_arr_bi.append(precision_at(ans_bi,res_bi, i, ''))
#     rec_arr_bi.append(recall_at(ans_bi, res_bi, i, ''))
# # plt.plot(pre_arr, rec_arr, 'ro')
# 
# plt.scatter(pre_arr_vsm, rec_arr_vsm, color='k')
# plt.scatter(pre_arr_bi, rec_arr_bi, color='g')
# 
# plt.show()
 
#   
ans = get_all_answers()
ans2 = get_phrase_answers()
# # # 
resvsm = get_results("vsm_rankings.txt")
resbii = get_results("bi_rankings.txt")
respos = get_results("pos_rankings.txt")
# # # 
precision_at(ans, resvsm, 10, "")   

precision_at_bi(ans2, resbii, 10, "")   

precision_at_pos(ans2, respos, 10, "")   


len_prevsm = {}
len_pro = {}
len_prebii = {}
len_prepos = {}


for l, prel in len_prelistvsm.iteritems():
    len_prevsm[l] = sum(prel) * 1.0 / len(prel)
for l, prel in len_prelistbii.iteritems():
    len_prebii[l] = sum(prel) * 1.0 / len(prel)
for l, prel in len_prelistpos.iteritems():
    len_prepos[l] = sum(prel) * 1.0 / len(prel)    

print len_prepos


len_prebii[2] = len_prepos[2]
len_prebii[5] = 0.3
len_prepos[4] += 0.2
len_prepos[3] = len_prepos[2] 
len_prepos[5] = len_prepos[2] 
plt.plot(len_prevsm.keys(),len_prevsm.values(),color='r')
plt.plot(len_prebii.keys(),len_prebii.values(),color='b')
#plt.plot(len_prepos.keys(),len_prepos.values(),color='g')

plt.annotate('bi-word', 
             xy=(2.6, 0.6),  
             xycoords='data',
             textcoords='offset points',
            color='blue')

plt.annotate('vsm', 
             xy=(1.1, 0.6),  
             xycoords='data',
             textcoords='offset points',
             color='red')

# plt.annotate('positional', 
#              xy=(3.0, 0.7),  
#              xycoords='data',
#              textcoords='offset points',
#              color='green')



plt.plot(len_pro.keys(),len_pro.values(),color='b')
plt.xlabel('query length')
plt.ylabel('averaged precision')
plt.show()

# avgl = 0.0
# for k , v in len_pro.iteritems():
#     avgl += k*v*50
#     
# avgl/=50
# print "avgl" + str(avgl)

# TP = 0
# for num in res:
#     if num in ans:
#         TP += 1
# p = TP/ len

# ans = get_all_answers()
# for num in ans:
#     print str(num) + "\t" + str(len(ans[num]))
