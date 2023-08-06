#__init__.py

__version__="1.1.6"

#imports

from random import random
import math
from random import randint


def riemannlist(start, end):
    theta = math.pi /3 
    arr = []
    length = end - start
    # Crazy exception case
    if(length == 0):
        rand = random()
        start = math.floor(length * rand)
        end  = start + length
               
     
    for i in range(start, length):
        y = theta * (1 + 6*i)
        y = math.sqrt((y/theta)**2 - 0.25)
        arr.append(y)
        y = theta* 5 *(1 + (6/5)*i)
        y = math.sqrt((y/theta)-0.25)
        arr.append(y)
        
    arr.sort()
    
    begin = 0
    fini = len(arr)-1
    
    for i in range(0, len(arr)-1):
        if arr[i] <= start:
                begin = i
        if arr[i] < end:
                fini = i
        if begin == 0:
            begin = begin +1
    
    
    arr = arr[begin-1:fini+1]
    
    
    return arr



def primelist(start, end):
    theta = math.pi /3 
    arr = []
    length = end - start
    
    if(length == 0):
        rand = random()
        start = math.floor(length * rand)
        end  = start + length
        
     
    for i in range(start, length):
        y = theta * (1 + 6*i)
        y = math.sqrt((y/theta)**2 - 0.25)
        arr.append(y)
        y = theta* 5 *(1 + (6/5)*i)
        y = math.sqrt((y/theta)-0.25)
        arr.append(y)
        
    arr.sort()

    prime = []
    for i in range(0, len(arr)-1):
        arr[i] = math.floor(arr[i])
        if(math.floor(arr[i]) % 2 != 0):
            arr[i] = arr[i] + 1
        prime.append(arr[i]+1)
        prime.append(arr[i]-1)
       
    prime.sort()
    
    primeh = []
    for i in range(0, len(prime)-1):
        if prime[i] not in primeh:
            primeh.append(prime[i])
    begin = 0
    fini = len(primeh)-1
    
    for i in range(0, len(primeh)-1):
        if primeh[i] <= start:
                begin = i
        if primeh[i] <= end:
                fini = i
        
    
    prime = primeh
    prime = prime[begin:fini]
    
    #set prime[0] = start
    #prime[len(prime)-1] = end
    #slice function copy into riemann list 
    return prime
      
      
      
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
    



def isprime(num):
    theta = math.pi/3
    r1 = num + 1
    r2 = num - 1
    length = math.ceil(num/2)
    arr = []
                
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
    
    return num in prime
        
    



def isriemann(num):
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
        
    
    return num in arr
        
        
        
    
        
        
    
     
    