import matplotlib.pyplot as plt
from build_load import load_queries
def precision_at(ans, res, n, cmd):
    TP = 0
    for query_num in res:
        resN = res[query_num][:n] #top N of result res[]
        numRel = len( set(resN) & set(ans[query_num]) )
        TP += numRel
        presN = numRel * 1.0 / n
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

pre_arr_vsm = [] 
rec_arr_vsm = [] 
pre_arr_bi = []
rec_arr_bi = []
ans_vsm = get_all_answers()
ans_bi = get_phrase_answers()
res_vsm = get_results('vsm_rankings.txt')
res_bi = get_results("bi_rankings.txt")         
for i in xrange(10,100):
    pre_arr_vsm.append(precision_at(ans_vsm, res_vsm, i, ''))
    rec_arr_vsm.append(recall_at(ans_vsm, res_vsm, i, ''))
    pre_arr_bi.append(precision_at(ans_bi,res_bi, i, ''))
    rec_arr_bi.append(recall_at(ans_bi, res_bi, i, ''))
# plt.plot(pre_arr, rec_arr, 'ro')

plt.scatter(pre_arr_vsm, rec_arr_vsm, color='k')
plt.scatter(pre_arr_bi, rec_arr_bi, color='g')

plt.show()
 

# ans = get_phrase_answers()
# 
# res = get_results("bi_rankings.txt")
# 
# recall_at(ans, res, 30000, "print")   
