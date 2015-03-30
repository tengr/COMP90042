q = {}
num = 0
query = ""
with open("/Users/ruichen/Documents/COMP90042/proj1/proj1data/06.topics.851-900.txt","r") as query_file:
    for line in query_file:
        if "<num>" in line:
            num = int(line.split()[-1])
        elif "<title>" in line:
            query = line.replace('<title>','').replace('"','').strip()
            q[num] = query
        
print q            
            
