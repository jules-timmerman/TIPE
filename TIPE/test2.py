from Client import Client
from Block import Block
import subprocess
import time


c0 = Client(8000, isFirstClient=True)

path = "D:\\Dev\\C++\\Visual Studio\\TIPE\\TIPE\\test.py"
N = 3
for i in range(1,N):
    subprocess.run(['start','cmd.exe', '@cmd', '/k', 'python', path, str(8000 + i)], shell=True)
    time.sleep(5)

