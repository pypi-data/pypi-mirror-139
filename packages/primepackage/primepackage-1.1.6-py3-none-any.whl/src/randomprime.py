import math 
from random import random, randint
def randomprime(seed = 100):

    theta = math.pi /3 
    arr = []
    
    length = seed
    
    for i in range(0, length):
        y = theta * (1 + 6*i)
        y = math.sqrt((y/theta)**2 - 0.25)
        arr.append(y)
        y = theta* 5 *(1 + (6/5)*i)
        y = math.sqrt((y/theta)-0.25)
        arr.append(y)
        
    arr.sort()

    prime = []
    for i in range(0, len(arr)):
        arr[i] = math.floor(arr[i])
        if(math.floor(arr[i]) % 2 != 0):
            arr[i] = arr[i] + 1
        prime.append(arr[i]+1)
        prime.append(arr[i]-1)
       
    prime.sort()
    
    primeh = []
    for i in range(0, len(prime)):
        if prime[i] not in primeh:
            primeh.append(prime[i])
        
        
    prime = primeh
    
    r = randint(0, len(prime)-1)
    
    result = prime[r]
    
    return result
    