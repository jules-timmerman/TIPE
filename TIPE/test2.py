from Client import Client
from Block import Block
from Transaction import Transaction
import subprocess
import time
import random


c0 = Client(8000, isFirstClient=True)

pathClient = "D:\\Travail\\Prépa\\TIPE Vevo\\TIPE\\TIPE\\test10.py"
NClient = 3
for i in range(1,NClient):
    subprocess.run(['start','cmd.exe', '@cmd', '/k', 'python', pathClient, str(8000 + i)], shell=True)
    time.sleep(5)

transs = []

for i in range(22):
	transs += [c0.createTrans(random.randint(0,2), random.randint(0,4) , str(random.randint(1,30)) + ";" + str(random.randint(1,12)) + ";" + str(random.randint(1970,2020)))]

print("E")


pathMiner = "D:\\Travail\\Prépa\\TIPE Vevo\\TIPE\\TIPE\\test11.py"
NMiner = 1
for i in range(NMiner):
    subprocess.run(['start','cmd.exe', '@cmd', '/k', 'python', pathMiner, str(9000 + i)], shell=True)
    time.sleep(5)

for t in transs:
    c0.sendTrans(t)
    time.sleep(2)


time.sleep(10)

for p in c0.listPerson:
    print(p.personToString())