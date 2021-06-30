from P2P import P2P
import socket
from Blockchain import Blockchain
from Block import Block
from hashlib import sha256
import threading
from Transaction import Transaction
import time

class Miner:

    refIP = "" # A REMPLIR AVEC LA FUTURE IP DU RASPBERRY EN GROS OU EN TOUT CAS D'UNE ENTITE DE REFERENCE QUI SERA TOUJOURS DANS LA CHAINE
    refPort = -1


    def __init__(self, port, firstIPs=[refIP], firstPorts=[refPort]):

        print("MINER "+ str(port))

        self.blockchain = Blockchain()
        self.transToBlock = []      # Liste de transactions à ajouter 

        self.idToMine = 0 # id du prochain bloc à miner (initialiser à 0 car incrémenter dans createThreadAndStart

        self.listPerson = [] # Liste de personne (pas forcément nécessaire mais la banane de TF2)

        self.pathToHopitalList = "listeHopital" + str(port) + ".txt" # Pour les tests utiles pour avoir différent .txt
        f = open(self.pathToHopitalList, "w")
        f.close()

        #self.p2p = P2P(socket.gethostbyname(socket.gethostname()), port, self.receivedData)
        self.p2p = P2P("127.0.0.1", port, self.receivedData)
        self.p2p.start()

        for i in range(len(firstIPs)):
                self.p2p.connect_with_node(firstIPs[i], firstPorts[i])
        self.sendData("getAllBlocks") # On récupère toute la chaîne du reste du réseau
        time.sleep(2)
        self.sendData("getHospitals") # On récupère la liste avec les clés
        time.sleep(2)
        self.sendData("getTotalClients") # On récupère le nombre total de client (et donc notre id à nous)
        time.sleep(2)

        self.miningThread = threading.Thread(target=self.block, args=(self))


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
            if self.blockchain.validBlocks != []:
                return {"command": "respondAllBlocks", "params": [self.blockchain.validBlocksToString()]}
        elif command == "respondAllBlocks":   # C'est la commande reçu après avoir fait getAllBlocks
            bc = Blockchain.stringToValidBlocks(params[0])
            
            #for b in bc:
            #    print(b.blockToString())
            #print("----------")
            #for bcs in self.blockchain.alternateFollowingChains:
            #    for b in bcs:
            #        print(b.blockToString())
            #    print("****************")

            # TODO : Certains blocs ont l'air d'être dupliqué (celui de départ n'est pas compté) donc à gérer

            if not self.blockchain.alreadyInAlternate(bc):
                self.blockchain.alternateFollowingChains += [bc]
        elif command == "getHospitals":
            return {"command": "respondHospitals", "params": [self.getHospitals()]}
        elif command == "respondHospitals":
            self.receiveAllHospitals(params[0])
        elif command == "newBlock":
            block = Block.stringToBlock(params[0])
            if block.isValidBlock():
                if block.blockId == self.blockchain.getLastValidBlock().blockId + 1: # Le nouveau bloc recu est le même que celui sur lequel on travaillait
                    self.miningThread.stop()    # TODO : En vrai il faudrait ne pas supprimer les transactions sur lesquels on travaillait pour pouvoir plutôt gérer sur les transactions présentes ou pas dans le bloc recu que l'id strictement
                    #self.idToMine += 1     # Gerer dans createThread...
                    if len(self.transToBlock) >= 5:
                        self.CreateAndStartThread()
                self.blockchain.addBlockToAlternateChain(block)
                self.blockchain.chainUpdate()


                if newLength > oldLength: # Pour pouvoir parse les nouveaux blocs valides
                    for i in range(oldLength, newLength):
                        self.parseBlock(self.blockchain.validBlocks[i])
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

        time.sleep(5)

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

    def getTotalClients(self):
        f = open(self.pathToHopitalList, "r")
        size = len(f.readlines())
        f.close()
        return size
    
    
    # MINER FUNCTIONS

    def addTransToBlock(self, trans):
        self.transToBlock += [trans]
        if len(self.transToBlock) >= 5:
            self.blockchain.chainUpdate()
            self.createAndStartThread()

    def block(self): 
        print("Starting to Mine")
        lb = self.blockchain.validBlocks[self.idToMine-1] # Last Block
        blockId = self.idToMine
        lbHash = lb.hashBlock()
        trans = self.transToBlock[0:5]
        self.transToBlock = self.transToBlock[5:]
        
        blockTemp = Block(blockId, lbHash, trans)

        print("Searching Proof of work for : " + blockTemp.blockToString())

        hashTemp = blockTemp.hashBlock()
        i = 0
        while hashTemp[0:Block.NZeros] != "0" * Block.NZeros:
            i += 1
            hashTemp = blockTemp.hashBlockWithPOW(i)
        blockTemp.proofOfWork = i

        #self.idToMine += 1 # Gerer dans createThread...
        self.blockchain.addBlockToAlternateChain(blockTemp)
        self.sendBlock(blockTemp)

    def sendBlock(self, blockTemp): # Envoie le bloc au reste de réseau (A FAIRE PLUS TARD)
        self.sendData("newBlock", [blockTemp.blockToString()])
        if len(self.transToBlock) >= 5:
            self.CreateAndStartThread()
    
    def receivedTrans(self,transaction) :
        signature = transaction.signature
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