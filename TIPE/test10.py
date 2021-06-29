from Client import Client
import time
import sys


startPort = 8000

# ********************************** 

#c0 = Client(startPort, isFirstClient=True)

#clients = [c0]
#miners = []
#N = 5

#for i in range(1, N):
#    clients += [Client(startPort + i, ["127.0.0.1"], [startPort])]
#    time.sleep(10)



#for c in clients:
#    print(c.idClient)
#    print(c.publicKey)


# **********************************

#c1 = Client (startPort+1, ["127.0.0.1"], [startPort])
#time.sleep(10)
#print(c1.idClient)


# *********************************

#c2 = Client (startPort+2, ["127.0.0.1"], [startPort])
#time.sleep(10)
#print(c2.idClient)



# *********************************

c = Client (int(sys.argv[1]), ["127.0.0.1"], [8000])
time.sleep(10)
print(c.idClient)
