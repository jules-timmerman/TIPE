from Client import Client
from Block import Block
from Transaction import Transaction
import subprocess
import time
import random


c0 = Client(8000, isFirstClient=True)

pathClient = "D:\\Dev\\C++\\Visual Studio\\TIPE\\TIPE\\test10.py"
N = 1
#for i in range(1,N):
#    subprocess.run(['start','cmd.exe', '@cmd', '/k', 'python', pathClient, str(8000 + i)], shell=True)
#    time.sleep(5)

transs = []

for i in range(12):
	transs += [c0.createTrans(random.randint(0,5), random.randint(0,4) , str(random.randint(1,30)) + "/" + str(random.randint(1,12)) + "/" + str(random.randint(1970,2020)))]

print("E")


pathMiner = "D:\\Dev\\C++\\Visual Studio\\TIPE\\TIPE\\test11.py"
for i in range(1,N):
    subprocess.run(['start','cmd.exe', '@cmd', '/k', 'python', pathMiner, str(8000 + i)], shell=True)
    time.sleep(5)

for t in transs:
    c0.sendTrans(t)
    time.sleep(5)
