from P2P import P2P
import socket
from Blockchain import Blockchain
from Block import Block
from hashlib import sha256
import threading


class Miner:

    refIP = "" # A REMPLIR AVEC LA FUTURE IP DU RASPBERRY EN GROS OU EN TOUT CAS D'UNE ENTITE DE REFERENCE QUI SERA TOUJOURS DANS LA CHAINE
    refPort = -1


    def __init__(self, port, firstIPs=[refIP], firstPorts=[refPort]):
        self.blockchain = Blockchain()
        self.transToBlock = []      # Liste de transactions à ajouter 

        self.p2p = P2P(socket.gethostbyname(socket.gethostname()), port, self.receivedData)
        #self.p2p = P2P("127.0.0.1", port, self.receivedData)
        self.p2p.start()

        for i in range(len(firstIPs)):
            self.p2p.connect_with_node(firstIPs[i], firstPorts[i])
        self.miningThread = threading.Thread(target=self.block, args=(self))

    def sendData(self, command, params): 
        """Envoie la commande à tout les pairs
        command: str avec la commande
        params: tableau de str avec les parametres"""

        contents = {"command": command, "params":params}

        self.p2p.sendData(contents)
        

    def receivedData(self, content):  
        command = contents["command"]
        params = contents["params"]


        if command == "getAllBlocks":   # Envoie l'entièreté de la blockchain au param1 
            return {"command": "respondAllBlocks", "content": [self.blockchain.validBlocksToString()]}
        elif command == "respondAllBlocks":   # C'est la commande reçu après avoir fait getAllBlocks
            self.blockchain.alternateFollowingChains += params[0]
        elif command == "getHospitals":
            return {"command": "respondHospitals", "content": [self.getHospitals()]}
        elif command == "respondHospitals":
            self.receiveAllHospitals(params[0])
        elif command == "newBlock":
            block = Block.stringToBlock(params[0])
            if block.isValidBlock():
                if block.blockId == self.blockchain.getLastValidBlock().blockId + 1: # Le nouveau bloc recu est le même que celui sur lequel on travaillait
                    self.miningThread.stop()
                    if len(self.transToBlock) >= 5:
                        self.CreateAndStartThread()
                self.blockchain.addBlockToAlternateChain(block)
                self.blockchain.chainUpdate()
        elif command == "getPerson":
            p = self.getPerson(params[0])
            if p != None:
                return {"command": "respondPerson", "content": [p.personToString()]}
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


        elif command == "addTransToBlock": # senderID puis transaction
            self.receivedTrans(params[0], params[1]) 


    def addTransToBlock(self, trans):
        self.transToBlock += trans
        if len(transToBlock >= 5):
            self.transToBlock = self.transToBlock[5:]
            #self.block() # Peut-être mettre dans un Thread plutôt 
            self.createAndStartThread()

    def block(self): 
        lb = self.blockchain.getLastValidBlock() # Last Block
        blockId = lb.blockId + 1
        lbHash = lb.hashBlock()
        trans = self.transToBlock[0:5]
        
        blockTemp = Block(blockId, lbHash, trans)

        hashTemp = blockTemp.hashBlock()
        i = 0
        while hashTemp[0:Block.NZeros] != "0" * Block.NZeros:
            i += 1
            hashTemp = blockTemp.hashBlockWithPOW(i)
        blockTemp.proofOfWork = i

        # Il faut envoyer le bloc aled
        self.sendBlock(blockTemp)

    def sendBlock(self, blockTemp): # Envoie le bloc au reste de réseau (A FAIRE PLUS TARD)
        self.sendData("newBlock", [blockTemp.blockToString()])
        if len(self.transToBlock) >= 5:
            self.CreateAndStartThread()
    
    def receivedTrans(self,senderId,transaction) :
        signature = transaction.signature
        f = open("listeHopital.txt", "r")
        publicKey = f[senderId]

        s = ""
        s += str(transaction.personId) + "|"
        s += str(transaction.maladieId) + "|"
        s += str(transaction.newDate) + "|"
        s += str(transaction.clientId) 
        
        hash = int.from_bytes(sha256(s).digest(), byteorder='big')
            
        hashFromSignature = pow(signature, publicKey[1], publicKey [0])
 
        if hashFromSignature == hash :
            self.addTransToBlock(transaction) 

        f.close()

    def getHospitals():
        f = open("listeHopital.txt", "r")
        s = ""
        for l in f:
            s += l
            s += "/"
        s = s[:-1]
        f.close()
        return s

    def receiveAllHospitals(s):
        linesOri = getHospitals().split("/")
        
        f = open("listeHopital.txt", "w")
        linesNew = s.split("/")


        lenOri,lenNew = len(linesOri), len(linesNew)
        min,max = min(lenOri, lenNew), max(lenOri, lenNew)

        for i in range(min):
            if linesOri[i] == "":
                f.write(linesOri[i])
            else:
                f.write(linesNew[i])

        if lenOri > lenNew:
            for i in range(min+1, lenOri):
                f.write(linesOri[i])
        else:
            for i in range(min+1, lenNew):
                f.write(linesNew[i])

    def createAndStartThread(self):
        self.miningThread = threading.Thread(target=self.block, args=(self))
        self.start()

    def getPerson(self, personId): # Renvoie un objet Person que l'on connait
        for p in self.listPerson:
            if p.personId == personId:
                return p
        return None