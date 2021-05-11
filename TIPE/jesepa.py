import time
import random

N = 100000
l = [k for k in  range(0,N)]

t1 = time.clock()
n = N - 1

v = l[0]
i = 0
while v != n:
    i += 1
    v = l[i]
t2 = time.clock()

print (t2 - t1)
print (i)
