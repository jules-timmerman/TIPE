from hashlib import sha256
from Block import Block
from Transaction import Transaction
import time
from Crypto.PublicKey import RSA
import random
from openpyxl import Workbook
import numpy as np
import matplotlib.pyplot as plt


keyPair = RSA.generate(bits=1024)

clepublique = [keyPair.n, keyPair.e]

cleprivee = [keyPair.n , keyPair.d ]



def hash(sum, pow): # Sum en str et pow un nombre
     s = bin(int.from_bytes(sha256(bytes(sum + str(pow), 'utf-8')).digest(), byteorder = "big"))[2:]
     s = (256-len(s))*'0' + s
     return s

t1 = Transaction(1,2,"10/02/2003",3,cleprivee)
t2 = Transaction(2,4,"10/02/1997",3,cleprivee)
t3 = Transaction(5,4,"10/06/1997",5,cleprivee)
t4 = Transaction(5,3,"01/06/1997",5,cleprivee)
t5 = Transaction(2,1,"01/06/2011",9,cleprivee)



b = Block(1,"000110101010101001011111",[t1,t2,t3,t4,t5])

N = 10**6

#for k in range(10):
#    t1 = time.time()
#    for i in range(N):
#        h = b.hashBlockWithPOW(i)
#        #print (h)
#    t2 = time.time()

Nz = 15

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

b.hashBlockWithPOW(100)

#try:


#    N = 10 ** 6

#    bool = True

#    workbook = Workbook()
#    sheet = workbook.active
#    res = [0]*N

#    for k in range(N) :
#        i = random.randint(0,10**Nz)
#        t1 = time.time()
#        bool = True
#        while bool :
#            h = b.hashBlockWithPOW(i)
#            if h[0:Nz] == Nz*"0" :
#                t2 = time.time()
#                #sheet["A"+str(k+2)] = (t2-t1)

#                #print(t2-t1)
#                res[int(((t2-t1)*100)//1)] += 1

#                if k % 1000 == 0:
#                    print(k)

#                bool = False
#            i += 1

#    print(res)

#    for k in range(0,N) :
#        sheet["B"+str(k+1)] = res[k]
#        sheet["A"+str(k+1)] = k

#except KeyboardInterrupt:
#    print("SAVING")
#    for k in range(0,k) :
#        sheet["B"+str(k+1)] = res[k]
#        sheet["A"+str(k+1)] = k



#workbook.save(filename="valeurs.xlsx")

# Test de l'influence de Nz sur la probabilité de trouver un bloc pendant Tmax :


Tmax = 7.54*(10**(-4))
Th = 2.5*(10**(-5))


def influsurtest1Nz(x) :
    return  1-(1-2**(-x))**(Tmax/Th)

Abs = np.linspace(0,100,2000)
Ord = influsurtest1Nz(Abs)

plt.plot(Abs,Ord)
plt.show()














