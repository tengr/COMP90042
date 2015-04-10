#most extreme element in an array
# def solution(a):
#     if len(a) == 0:
#         return -1
#     else:
#         avg = sum(a) * 1.0 / len(a)
#         ind = -1
#         diff = 0
#         for i in xrange(len(a)):
#             temp_diff = a[i] - avg
#             if temp_diff < 0:
#                 temp_diff = -temp_diff
#             print temp_diff
#             if temp_diff >= diff:
#                 diff = temp_diff
#                 ind = i
#     return ind

def solution(A):
    if len(A) == 0:
        return -1
    ind = 0
    s = A[0]
    min_ind = 0
    max_ind = 0
    for i in xrange(1,len(A)):
        s += A[i]
        if A[i] < A[min_ind]:
            min_ind = i
        elif A[i] > A[max_ind]: 
            max_ind = i
    if A[max_ind] - s * 1.0 / len(A) > s * 1.0 / len(A) - A[min_ind]:
        ind = max_ind
    else:
        ind = min_ind
    return ind 
    
    
test = [-4,-9,3,10]
print(solution(test))