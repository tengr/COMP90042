import sys
import time

max1 = 10000000
max2 = 10000000
nn = {}
nn[max1] = max2

def minus(zidian):
    zidian[max1] = zidian[max1] - 1

def decorator(k, zidian):
    k(zidian)
    
start_time = time.time()   
while(nn[max1] > 0):
    nn[max1] = nn[max1] - 1
print("no function call --- %s seconds ---" % (time.time() - start_time))

nn[max1] = max2

start_time = time.time()
while(nn[max1] > 0):
    decorator(minus,nn)   
print("with function call --- %s seconds ---" % (time.time() - start_time))
    
    