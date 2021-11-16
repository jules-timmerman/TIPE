from hashlib import sha256
from Block import Block
from Transaction import Transaction
import time
from Crypto.PublicKey import RSA

def hash(sum, pow): # Sum en str et pow un nombre
     s = bin(int.from_bytes(sha256(bytes(sum + str(pow), 'utf-8')).digest(), byteorder = "big"))[2:]
     s = (256-len(s))*'0' + s
     return s

t1 = Transaction(1,2,"10/02/2003",3)
t2 = Transaction(2,4,"10/02/1997",3)
t3 = Transaction(5,4,"10/06/1997",5)
t4 = Transaction(5,3,"01/06/1997",5)
t5 = Transaction(5,3,"01/06/2007",5)



b = Block(1,"bonjour",)

N = 10**6

#for k in range(10):
#    t1 = time.time()
#    for i in range(N):
#        h = b.hashBlockWithPOW(i)
#        #print (h)
#    t2 = time.time()

Nz = 7


#for i in range(20):
#    t1 = time.time()
#    bool = True
#    i = 0
#    while bool :
#        h = b.hashBlockWithPOW(i)
#        if h[0:Nz] == Nz*"0" :
#            bool = False
#        #print(h)
#        i += 1
#    bool = True      
#    t2 = time.time()


#    t = t2 - t1
#    print(t)


for i in range(20):
    t1 = time.time()
    bool = True
    i = 0
    while bool :
        h = b.hashBlockWithPOW(i)
        if h[0:Nz] == Nz*"0" :
            bool = False
        i += 1
    print(i-1)
    bool = True      
    t2 = time.time()


    t = t2 - t1
    print(t)