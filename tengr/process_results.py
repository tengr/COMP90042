ans = {} 
res = {}
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
# for query_num in ans:
#     print str(query_num) + "\t" + str(len(set(res[query_num]) & set(ans[query_num])))

#top 10
TP = 0
for query_num in ans:
    #ans10 = ans[query_num][:10]
    res10 = res[query_num][:10]
    #print ans[query_num]
    rel_num = len( set(res10) & set(ans[query_num]) )
    #print str(rel_num)
    TP += rel_num
    pres10 = rel_num / 10.0
    print str(query_num) + "\t" + str(pres10) + "\n"
    
precision = TP / (len(ans) * 10.0)

print "TP = " + str(TP)
 
print "queries = " + str(len(ans))  
print "overall precision = " + str(precision)