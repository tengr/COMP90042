# #returning length of array with more 0s than 1s ending in ind
# 
# 
# def solution(A, n):
#     s = 0
#     sum_arr = []
#     for i in xrange(len(A)):
#         s += A[i]
#         sum_arr.append(s)
#     
#     one_offset = 0
#     zero_offset = 0
#     digits_in_between = 0 #digits between left most zero and right most one
# 
#     for i in xrange(len(A)):
#         if(A[i] == 1):
#             one_offset += 1  #how many ones from the left
#         else:
#             break
#     left_most_zero = one_offset        
#     
#     for j in reversed(xrange(len(A))):
#         if(A[j] == 0):
#             zero_offset += 1 #how many zeros from the right
#         else:
#             break
#     right_most_one = len(A) - zero_offset - 1
#     
#     digits_in_between = right_most_one - 1 - left_most_zero
#     
#     if right_most_one < left_most_zero:
#         return -1
#     elif left_most_zero == 0 and right_most_one == len(A) - 1:
#         return len(A)
#     else: #must have solution
# #         digits_in_between = right_most_one - 1 - left_most_zero
# #         num_ones_inbetween = sum_arr[right_most_one - 1] - sum_arr[left_most_zero]
# #         num_zeros_inbetween = digits_in_between - num_ones_inbetween
# #         zero_flag = -1 #seen zero
# #         one_flag = -1 #seen one
# #         one_leftof_zero = 0
# #         one_rightof_zero
# #         max_zero_ind = left_most_zero
# #         metric = 0
# #         max_zero = 0
# #         for i in xrange(left_most_zero + 1, right_most_one):
# #             if(A[i] == 0):
# #                 metric += 1
# #             else:
# #                 metric -= 1
# #             if (metric > max_zero):
# #                 max_zero = metric
# #                 max_zero_ind = i
# #         
# #         max_one_ind = right_most_one        
# #         metric = 0
# #         max_one = 0
# #         for i in reversed(xrange(left_most_zero + 1, right_most_one)):
# #             if(A[i] == 1):
# #                 metric += 1
# #             else:
# #                 metric -= 1
# #             if (metric > max_one):
# #                 max_one = metric
# #                 max_one_ind = i
# #                 
# #         if max_zero_ind < max_one_ind:
# #             one_left = one_offset - max_zero > 0 ? one_offset - max_zero : 0
# #             zero_left = zero_offset - max_one > 0 ? zero_offset - max_one : 0
# #            return len(A) - one_left - zero_left
# #         else:
#             max_len = digits_in_between + 2
#             #print str(left_most_zero) + "\t" + str(right_most_one)
#             #print str(digits_in_between)
#             for i in xrange(left_most_zero + 1, right_most_one):
#                 left_ones = sum_arr[i - 1] - sum_arr[left_most_zero] # number of ones from i - 1 to left_most_zero
#                 between = i - 1 - left_most_zero #digits in between
#                 left_zeros = between - left_ones  # number of zeros from i - 1 to left_most_zero
#                
#                 right_ones = sum_arr[right_most_one - 1] - sum_arr[i - 1] #number of ones from right_most_one to i
#                 between = right_most_one  - i #(right_most_one - 1) - (i - 1)
#                 right_zeros = between - right_ones 
#                 
#                 #print str(right_ones) + "\t" + str(right_zeros)
#                 #print str(between)
#                 
#                 if (left_zeros >= left_ones and right_ones >= right_zeros): # it is a valid division
#                     #print "valid"
#                     l = digits_in_between + 2
#                     l += min((left_zeros - left_ones), one_offset )
#                     l += min((right_ones - right_zeros), zero_offset)
#                     if l > max_len:
#                         max_len = l
#             return max_len
                    
#test = [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0]
# test = [1,1,1,0,0,0,1,1,1,0,0]
# print solution(test, 6)


#returning length of array with more 0s than 1s ending in ind


def solution(A):
    s = 0
    sum_arr = []
    for i in xrange(len(A)):
        s += A[i]
        sum_arr.append(s)
    
    one_offset = 0
    zero_offset = 0
    
    for i in xrange(len(A)):
        if(A[i] == 1):
            one_offset += 1  #how many ones from the left
        else:
            break
    left_most_zero = one_offset        
    
    for j in reversed(xrange(len(A))):
        if(A[j] == 0):
            zero_offset += 1 #how many zeros from the right
        else:
            break
    right_most_one = len(A) - zero_offset - 1
    
    digits_in_between = right_most_one - 1 - left_most_zero #digits between left most zero and right most one
    
    if right_most_one < left_most_zero:
        return 0
    elif left_most_zero == 0 and right_most_one == len(A) - 1:
        return len(A)
    else: 
        max_len = digits_in_between + 2

        for i in xrange(left_most_zero, right_most_one + 1):
            left_ones = sum_arr[i - 1] - sum_arr[left_most_zero] # number of ones from i - 1 to left_most_zero
            between = i - 1 - left_most_zero #digits in between
            left_zeros = between - left_ones  # number of zeros from i - 1 to left_most_zero
           
            right_ones = sum_arr[right_most_one - 1] - sum_arr[i - 1] #number of ones from right_most_one to i
            between = right_most_one  - i #(right_most_one - 1) - (i - 1)
            right_zeros = between - right_ones 
            
            if (left_zeros >= left_ones and right_ones >= right_zeros): # it is a valid division

                l = digits_in_between + 2
                l += min((left_zeros - left_ones), one_offset )
                l += min((right_ones - right_zeros), zero_offset)
                if l > max_len:
                    max_len = l
        return max_len
                    
#test = [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0]
test = [1,1,1,0,0,0,1,1,1,0,0]
print solution(test)
                        