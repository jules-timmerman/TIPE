from Client import Client
from Miner import Miner
import time

startPort = 8000
c0 = Client(startPort)
c0.idClient = 0

clients = []
miners = []
N = 5

for i in range(1, N):
    clients += [Client(startPort + i, ["127.0.0.1"], [startPort])]

time.sleep(300)

for c in clients:
    print(c.idClient)



