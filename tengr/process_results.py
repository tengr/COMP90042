import matplotlib.pyplot as plt
ans = {} 
res = {}
def precision_at(n, cmd):
    TP = 0
    for query_num in ans:
        resN = res[query_num][:n] #top N of result res[]
        numRel = len( set(resN) & set(ans[query_num]) )
        TP += numRel
        presN = numRel * 1.0 / n
        if cmd == 'print':
            print str(query_num) + "\t" + str(presN) + "\n"
        
    precision = TP / (len(ans) * n * 1.0)
    if cmd == 'print':
        print "TP = " + str(TP)    
        print "queries = " + str(len(ans))  
        print "overall precision = " + str(precision)
    return precision

def recall_at(n, cmd):
    TP = 0
    for query_num in ans:
        resN = res[query_num][:n] #top N of result res[]
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

with open('/Users/ruichen/Documents/COMP90042/proj1/proj1data/qrels.february','r') as f1:
    for line in f1:
        arr = line.split()
        query_num = arr[0]
        relevance = int(arr[-1])
        filename = arr[2]
        if relevance > 0:
            if query_num in ans:
                ans[query_num].append(filename)
            else:
                ans[query_num] = [filename]



with open('/Users/ruichen/Documents/workspace/IR/tengr/rankings.txt', 'r') as f2:
    for line in f2:
        arr = line.split()
        query_num = arr[0]
        filename = arr[2].replace(".txt", "")
        if query_num in res:
            res[query_num].append(filename)
        else:
            res[query_num] = [filename]

pre_arr = [] 
rec_arr = []           
for i in xrange(10,101):
    pre_arr.append(precision_at(i, ''))
    rec_arr.append(recall_at(i, ''))
plt.plot(pre_arr, rec_arr, 'ro')
plt.show()
    
