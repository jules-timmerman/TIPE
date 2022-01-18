from Client import Client
from Transaction import Transaction
import random as rd 


nbMaladies = 20
nbClients = 0
nbPatients = 20
startPort = 8000
listeClients = []


try :
    while True :
        rand = rd.random() 
        if rand < 0.1 :
            listeClients += Client (startPort+nbClients, ["127.0.0.1"], [startPort])
            nbClients += 1
        if nbClients > 4 :
            rand = rd.random()
            if rand < 0.2 :
                idClient = rd.randint(0,nbClients)
                trans = Transaction.randTrans(nbPatients, nbMaladies, idClient)
                listeClients[idClient].
                

        
        



except KeyboardInterrupt:
    print("Simulation finie :) ")