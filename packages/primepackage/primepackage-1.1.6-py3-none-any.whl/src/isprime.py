import math
from random import random, randint

def primelist(num1 = 1, num2 = 100, length = 99):
    
    
    import math
    import numpy as np
    theta = math.pi /3 
    arr = []
    
    
    # Crazy exception case
    if(length == 0):
        length = abs(num2 - num1)
    elif (length > 0):
        rand = random()
        num1 = math.floor(length * rand)
        num2  = num1 + length
               
     
    for i in range(0, length):
        y = theta * (1 + 6*i)
        y = math.sqrt((y/theta)**2 - 0.25)
        arr.append(y)
        y = theta* 5 *(1 + (6/5)*i)
        y = math.sqrt((y/theta)-0.25)
        arr.append(y)
        
    arr.sort()

        # if count > 0:
        #     for j in range(0, len(arr)):
        #         del arr[j]
            
       
      
        # if  np.where(arr == x) > 0:
        #     for j in range(1, len(x)):
        #         arr.remove[arr[x]]
    prime = []
    for i in range(0, len(arr)):
        arr[i] = math.floor(arr[i])
        if(math.floor(arr[i]) % 2 != 0):
            arr[i] = arr[i] + 1
        prime.append(arr[i]+1)
        prime.append(arr[i]-1)
       
    prime.sort()
    
    print("Finidng duplicates")
    primeh = []
    for i in range(0, len(prime)):
        if prime[i] not in primeh:
            primeh.append(prime[i])
        
        
    prime = primeh
    
    #remove duplicates # double loop option
    # test = [x for x in arr if x== arr[i]]
    # for i in range(0, len(arr)):
    #     if test > 1:
    #         arr.remove(arr[i])
    
    
    
    return prime
        
    