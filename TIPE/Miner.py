from typing import List
from P2P import P2P
import socket
from Blockchain import Blockchain
from Block import Block
from hashlib import sha256
import threading
from Transaction import Transaction
import time
from Maladie import Maladie
import random


class Miner:

    refIP = "127.0.0.1"
    refPort = 9000


    def __init__(self, port, firstIPs=[refIP], firstPorts=[refPort]):

        print("MINER "+ str(port))

        self.port = port

        self.blockchain = Blockchain()
        self.transToBlock : List[Transaction] = []     # Liste de transactions à ajouter 
        self.lastMinedBlock = Block(0,0,[],0) # Le dernier bloc miné (pour avoir accès aux valeurs quand on mine)

        self.idToMine = 0 # id du prochain bloc à miner (initialiser à 0 car incrémenter dans createThreadAndStart
        self.newFound = False # Ce qui nous permettra de couper le Thread en cours

        self.listPerson = []

        self.pathToHopitalList = "listeHopital" + str(port) + ".txt" # Pour les tests utiles pour avoir différent .txt
        f = open(self.pathToHopitalList, "w")
        f.close()

        #self.p2p = P2P(socket.gethostbyname(socket.gethostname()), port, self.receivedData)
        self.p2p = P2P("127.0.0.1", port, self.receivedData)
        self.p2p.start()

        for i in range(len(firstIPs)): # On se connecte aux référents
            self.p2p.connect_with_node(firstIPs[i], firstPorts[i])
        self.sendData("getAllBlocks") # On récupère toute la chaîne du reste du réseau
        time.sleep(2)
        self.sendData("getHospitals") # On récupère la liste avec les clés
        time.sleep(2)
        self.sendData("getTotalClients") # On récupère le nombre total de client (et donc notre id à nous)
        time.sleep(2) 

        self.miningThread = threading.Thread(target=self.block)


    def sendData(self, command, params = []): 
        """Envoie la commande à tout les pairs
        command: str avec la commande
        params: tableau de str avec les parametres"""

        contents = {"command": command, "params":params}

        self.p2p.sendData(contents)
        

    def receivedData(self, contents):  
        command = contents["command"]
        params = contents["params"]

        if command == "getAllBlocks":
            if self.blockchain.validBlocks != [] and self.blockchain.alternateFollowingChains != []:
                return {"command": "respondAllBlocks", "params": [self.blockchain.validBlocksToString(), self.blockchain.alternateFollowingChainsToString()]}
            elif self.blockchain.validBlocks != []:
                return {"command": "respondAllBlocks", "params": [self.blockchain.validBlocksToString(), ""]}

        elif command == "respondAllBlocks":   # C'est la commande reçu après avoir fait getAllBlocks
            bc = Blockchain.stringToValidBlocks(params[0])
            if not self.blockchain.alreadyInAlternate(bc):
                self.blockchain.addBlocksToAlternateChain(bc)
            if params[1] != "":
                alternate = Blockchain.stringToAlternateFollowingChains(params[1])
                for l in alternate:
                    if not self.blockchain.alreadyInAlternate(l):
                        self.blockchain.addBlocksToAlternateChain(l)
        elif command == "getHospitals":
            return {"command": "respondHospitals", "params": [self.getHospitals()]}
        elif command == "respondHospitals":
            self.receiveAllHospitals(params[0])
        elif command == "newBlock":
            block = Block.stringToBlock(params[0])
            print(str(self.port) + " VALID : " + str(block.isValidBlock()))
            if block.isValidBlock():
                if block.blockId == self.blockchain.getLastValidBlock().blockId + 1: # Le nouveau bloc recu est le même que celui sur lequel on travaillait
                    print(str(self.port) + " received SAME that the one mining")
                    self.stopMining()
                    
                    self.lastMinedBlock = block
                    if len(self.transToBlock) >= 5:
                        self.createAndStartThread()
                self.blockchain.addBlockToAlternateChain(block)
                self.blockchain.chainUpdate()
        elif command == "getPerson":
            p = self.getPerson(params[0])
            if p != None:
                return {"command": "respondPerson", "params": [p.personToString()]}
        elif command == "respondPerson":
            person = Person.stringToPerson(params[0])
            isFound = False
            for p in self.listPerson:
                if p.personId == person.personId:
                    isFound = True
                    if len(p.medicalHistory) < len(person.medicalHistory):
                        p = person
            if not isFound:
                self.listPerson += person
        elif command == "getTotalClients":
            return {"command": "respondTotalClients", "params": [self.getTotalClients()]}
        elif command == "notifyAll":
            newId = params[0]
            newPK = params[1]
            self.noticeNew(newId, newPK)


        elif command == "addTransToBlock": # senderID puis transaction
            self.receivedTrans(Transaction.stringToTrans(params[0])) 



    # SHARED FUNCTIONS
    def getPerson(self, personId): # Renvoie un objet Person que l'on connait
        for p in self.listPerson:
            if p.personId == personId:
                return p
        return None

    def getUnknownPerson(self, personId):
        self.sendData("getPerson", [personId])
        time.sleep(1)
        return self.getPerson(personId)

    def getHospitals(self):
        f = open(self.pathToHopitalList, "r")
        s = ""
        for l in f:
            s += l.strip('\n')
            s += "/"
        s = s[:-1]
        f.close()
        return s

    def receiveAllHospitals(self, s):
        linesOri = self.getHospitals().split("/")
        
        f = open(self.pathToHopitalList, "w")
        linesNew = s.split("/")

        lenOri,lenNew = len(linesOri), len(linesNew)
        low = min(lenOri, lenNew)

        for i in range(low):
            if linesOri[i] == "":
                f.write(linesNew[i] + '\n')
            else:
                f.write(linesOri[i] + '\n')

        if lenOri > lenNew:
            for i in range(low, lenOri):
                f.write(linesOri[i] + '\n')
        else:
            for i in range(low, lenNew):
                f.write(linesNew[i] + '\n')
        f.close()

    def getTotalClients(self):
        f = open(self.pathToHopitalList, "r")
        size = len(f.readlines())
        f.close()
        return size

    def noticeNew(self, newId, newPK):
        s = '/' * newId + newPK
        self.receiveAllHospitals(s)
    
    
    # MINER FUNCTIONS

    def addTransToBlock(self, trans):
        self.transToBlock += [trans]
        if len(self.transToBlock) >= 5 and not self.miningThread.is_alive(): # On ne veut pas miner deux blocs à la fois
            self.blockchain.chainUpdate()
            self.createAndStartThread()
    
    def stopMining(self):
        print(str(self.port) + " mining thread : " + str(self.miningThread.is_alive()))
        if self.miningThread.is_alive():
            self.newFound = True
            self.miningThread.join()

    def shouldStop(self):
        return self.newFound
    
    def block(self): 
        print(str(self.port) + " : Starting to Mine")
        blockId = self.idToMine
        lbHash = self.lastMinedBlock.hashBlock()
        trans = self.transToBlock[0:5]
        self.transToBlock = self.transToBlock[5:]
        
        blockTemp = Block(blockId, lbHash, trans)

        print(str(self.port) + " : Searching Proof of work for : " + blockTemp.blockToString())

        hashTemp = blockTemp.hashBlock()
        i = random.randint(0,10**6)
        s = "0" * Block.NZeros
        while (hashTemp[0:Block.NZeros] != s) and (not self.shouldStop()):
            i += 1
            hashTemp = blockTemp.hashBlockWithPOW(i)

        if self.newFound: # Si quelqu'un à trouvé le bloc avant nous
            self.newFound = False
            print(str(self.port) + " s'arrete prematurement")
        else:
            print("\n\n" + str(self.port) + " A TROUVE LA POW\n\n")
            blockTemp.proofOfWork = i

            self.lastMinedBlock = blockTemp
            self.blockchain.addBlockToAlternateChain(blockTemp)
            self.blockchain.chainUpdate()
            self.sendBlock(blockTemp)       

    def sendBlock(self, blockTemp): # Envoie le bloc au reste de réseau
        self.sendData("newBlock", [blockTemp.blockToString()])
        if len(self.transToBlock) >= 5:
            self.createAndStartThread()
    
    def receivedTrans(self,transaction) :
        signature = transaction.signature # On va vérifier si la signature est valide
        f = open(self.pathToHopitalList, "r")
        publicKey = f.readlines()[transaction.clientId].split('%')

        s = ""
        s += str(transaction.personId) + "|"
        s += str(transaction.maladieId) + "|"
        s += str(transaction.newDate) + "|"
        s += str(transaction.clientId) 
        
        hash = int.from_bytes(sha256(bytes(s, 'utf-8')).digest(), byteorder='big')
            
        hashFromSignature = pow(signature, int(publicKey[1]), int(publicKey[0]))
 
        if hashFromSignature == hash :
            self.addTransToBlock(transaction) 

        f.close()

    def createAndStartThread(self):
        self.idToMine += 1
        self.miningThread = threading.Thread(target=self.block)
        self.miningThread.start()