import matplotlib.pyplot as plt
import numpy as np


Th = 2.35115 * (10 **(-3))
Nz = 15
Ph = 2 ** (-Nz)
dt = 2 # On travaille en centièmes de seconde

# P(t1, t2) = (1-Ph)^(t1/Th) x (1 - (1-Ph)^((t2-t1) /Th))



def f(t1,t2, Ph = Ph, Th = Th): 
    return ((1-Ph)**(t1/Th)) * (1 - (1 - Ph)**((t2-t1) / Th))

X = np.linspace(0,1500,1500)
Y = f(X, X + dt)

plt.plot(X,Y)
plt.show()