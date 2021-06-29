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
            return {"command": "respondAllBlocks", "params": [self.blockchain.validBlocksToString()]}
        elif command == "respondAllBlocks":   # C'est la commande reçu après avoir fait getAllBlocks
            self.blockchain.alternateFollowingChains += params[0]
        elif command == "getHospitals":
            return {"command": "respondHospitals", "params": [self.getHospitals()]}
        elif command == "respondHospitals":
            self.receiveAllHospitals(params[0])
        elif command == "newBlock":
            block = Block.stringToBlock(params[0])
            time.sleep(5) # On attends de traiter les réponses
            if block.isValidBlock():
                oldLength = len(self.blockchain.validBlocks) # On va s'interesser au changement de taille
                self.blockchain.addBlockToAlternateChain(block)
                self.blockchain.chainUpdate()
                newLength = len(self.blockchain.validBlocks) 

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
        elif command == "respondTotalClients":
            if self.idClient == -1: # Pour ignorer les requêtes suivantes à notre première réponse (supposée correcte)
                self.idClient = params[0]
                f = open(self.pathToHopitalList, "a")
                f.write(str(self.publicKey[0]) + "%" + str(self.publicKey[1]) + '\n')
                f.close()
                self.sendData("respondHospitals", [self.getHospitals()])



        elif command == "addTransToBlock": # senderID puis transaction
            self.receivedTrans(params[0], params[1]) 



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
        self.transToBlock += trans
        if len(transToBlock >= 5):
            #self.block() # Peut-être mettre dans un Thread plutôt 
            self.createAndStartThread()

    def block(self): 
        lb = self.blockchain.getLastValidBlock() # Last Block
        blockId = lb.blockId + 1
        lbHash = lb.hashBlock()
        trans = self.transToBlock[0:5]
        self.transToBlock = self.transToBlock[5:]
        
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

    def createAndStartThread(self):
        self.miningThread = threading.Thread(target=self.block, args=(self))
        self.start()