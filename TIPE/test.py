from Client import Client
from Miner import Miner
import time

startPort = 8000

# ********************************** 

#c0 = Client(startPort, isFirstClient=True)

#clients = [c0]
#miners = []
#N = 1

#for i in range(1, N):
#    clients += [Client(startPort + i, ["127.0.0.1"], [startPort])]
#    time.sleep(10)



#for c in clients:
#    print(c.idClient)
#    print(c.publicKey)


# **********************************

c1 = Client (startPort+1, ["127.0.0.1"], [startPort])
time.sleep(10)
print(c1.idClient)

