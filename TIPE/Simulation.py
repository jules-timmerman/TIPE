from Client import Client
from Transaction import Transaction
import random as rd 
import time
from Miner import Miner
from Blockchain import Blockchain

nbMinCli = 0
nbMiners = 0
nbMaladies = 20
nbClients = 0
nbPatients = 20
startPort = 8000
listeClients = []
listeMiners = []

boolOk = True


def simulate() : #A mettre dans un thread à part ...

    try :
        while boolOk :

            rand = rd.random() 
            if (rand < 0.05) or (nbClients < 5)  :
                listeClients += [Client(startPort+nbMinCli)]
                nbClients += 1
                nbMinCli += 1
            
            rand = rd.random()
            if (rand < 0.05) or (nbMiners < 5) :
                listeMiners += [Miner(startPort+nbMinCli)]
                nbMiners += 1
                nbMinCli += 1

            
            if (nbClients > 4) and (nbMiners > 4) :
                rand = rd.random()
                if rand < 0.8 :
                    idClient = rd.randint(0,nbClients)
                    trans = Transaction.randTrans(nbPatients, nbMaladies, idClient)
                    listeClients[idClient].sendTrans(trans)
            time.sleep(10)  

    except KeyboardInterrupt:
        print("Simulation finie :) ")

def pause() : 
    boolOk = not boolOk

def generateFakeTrans() :
    boolOk = False
    idClient1 = rd.randint(0, nbClients)
    idClient2 = idClient1
    while idClient1 == IdClient2 :
        idClient2 = rd.randint(0,nbClients)
    trans = Transaction.randTrans(nbPatients, nbMaladies, idClient1)
    listeClients[idClient2].sendTrans(trans)


def generateTrans() :
    boolOk = False
    idClient = rd.randint(0,nbClients)
    trans = Transaction.randTrans(nbPatients, nbMaladies, idClient)
    listeClients[idClient].sendTrans(trans)

def generateClient():
    boolOk = False
    listeClients += [Client (startPort+nbMinCli)]
    nbClients += 1
    nbMinCli += 1

def generateMiner() : 
    boolOk = False
    listeMiners += [Miner(startPort+nbMinCli)]
    nbClients += 1
    nbMiners += 1

def clientkChainState(k) :
    return listeClients[k].blockchain.validBlocks

def clientkAlternateChainState(k) :
    return listeClients[k].alternateFollowingChains

def minerkChainState(k) :
    return listeMiners[k].blockchain.validBlocks

def minerkAlternateChainState(k) :
    return listeMiners[k].alternateFollowingChains














