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
pre_arr_ro = []
rec_arr_ro = []
pre_arr_lm = []
rec_arr_lm = []
pre_arr_piv = []
rec_arr_piv = []
ans = get_all_answers()
#ans_bi = get_phrase_answers()
res_vsm = get_results('vsm_rankings.txt')
res_ro = get_results("10roch_vsm_rankings.txt")
res_lm = get_results("lm_vsm_rankings.txt")
res_piv = get_results("pivot_vsm_rankings.txt")         
for i in xrange(10,100):
    pre_arr_vsm.append(precision_at(ans, res_vsm, i, ''))
    rec_arr_vsm.append(recall_at(ans, res_vsm, i, ''))
    pre_arr_ro.append(precision_at(ans,res_ro, i, ''))
    rec_arr_ro.append(recall_at(ans, res_ro, i, ''))
    pre_arr_lm.append(precision_at(ans,res_lm, i, ''))
    rec_arr_lm.append(recall_at(ans, res_lm, i, ''))
    pre_arr_piv.append(precision_at(ans,res_piv, i, ''))
    rec_arr_piv.append(recall_at(ans, res_piv, i, ''))
    
for i in range(len(pre_arr_vsm)):
    pre_arr_vsm[i] = max(pre_arr_vsm[i:])
    rec_arr_vsm[i] = min(rec_arr_vsm[i:])
    pre_arr_ro[i] = max(pre_arr_ro[i:])
    rec_arr_ro[i] = min(rec_arr_ro[i:])
    pre_arr_lm[i] = max(pre_arr_lm[i:])
    rec_arr_lm[i] = min(rec_arr_lm[i:])
    pre_arr_piv[i] = max(pre_arr_piv[i:])
    rec_arr_piv[i] = min(rec_arr_piv[i:])

plt.plot(rec_arr_vsm, pre_arr_vsm, 'k')
plt.plot(rec_arr_ro, pre_arr_ro, color='b')
plt.plot(rec_arr_piv, pre_arr_piv, color='r')
plt.plot(rec_arr_lm, pre_arr_lm, color='g')

plt.annotate('Original vsm', 
             xy=(0.26, 0.58),  
             xycoords='data',
             textcoords='offset points',
             color='b')

plt.annotate('Rocchio\'s Algo', 
             xy=(0.26, 0.56),  
             xycoords='data',
             textcoords='offset points',
            color='b')

plt.annotate('Pivoted doc length', 
             xy=(0.26, 0.54),  
             xycoords='data',
             textcoords='offset points',
            color='r')

plt.annotate('Language model', 
             xy=(0.26, 0.52),  
             xycoords='data',
             textcoords='offset points',
            color='g')


plt.xlabel('Interpolated recall')
plt.ylabel('Interpolated precision')

plt.show()


    
 
#   
# ans = get_all_answers()
# # # # 
# res = get_results("nsns_vsm_rankings.txt")
# # # # 
# precision_at(ans, res, 10, "print")   

# ans = get_all_answers()
# for num in ans:
#     print str(num) + "\t" + str(len(ans[num]))
