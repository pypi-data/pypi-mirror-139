import math
from random import random, randint
def isriemann(num):
    import math
    theta = math.pi/3
    length = math.ceil(num/2)
    arr = []
    result = False
    
    for i in range(0, length):
        y = theta * (1 + 6*i)
        y = math.sqrt((y/theta)**2 - 0.25)
        arr.append(y)
        y = theta* 5 *(1 + (6/5)*i)
        y = math.sqrt((y/theta)-0.25)
        arr.append(y)
        
    arr.sort()
    
    for i in range(0, len(arr)):
        if math.floor(arr[i]) % 2 != 0:
            arr[i] = arr[i] + 1
    
    for i in range(0, len(arr)):
        arr[i] = math.floor(arr[i])
        
    test1 = [x for x in arr if x == num]
    print(test1)
    if test1 is not None:
        result = True
    
    return result
        
        
        
    
    