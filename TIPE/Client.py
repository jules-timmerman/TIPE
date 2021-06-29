from P2P import P2P
import socket
from Blockchain import Blockchain
from Crypto.PublicKey import RSA
from hashlib import sha256
from Person import Person
import time


class Client:
    
    refIP = "" # A REMPLIR AVEC LA FUTURE IP DU RASPBERRY EN GROS OU EN TOUT CAS D'UNE ENTITE DE REFERENCE QUI SERA TOUJOURS DANS LA CHAINE
    refPort = -1


    def __init__(self, port, firstIPs=[refIP], firstPorts=[refPort], isFirstClient = False): # firstIPs est un tableau de premiers pairs à qui se connecter idem firstPorts
        self.blockchain = Blockchain()
        self.listPerson = []  
        
        keyPair = RSA.generate(bits=1024)

        self.publicKey =  [keyPair.n, keyPair.e]
        self.privateKey = [keyPair.n, keyPair.d]

        self.pathToHopitalList = "listeHopital" + str(port) + ".txt" # Pour les tests utiles pour avoir différent .txt
        f = open(self.pathToHopitalList, "w")
        f.close()

        #self.p2p = P2P(socket.gethostbyname(socket.gethostname()), port, self.receivedData)
        self.p2p = P2P("127.0.0.1", port, self.receivedData)
        self.p2p.start()


        if isFirstClient:
            self.idClient = 0
            f = open(self.pathToHopitalList, "w")
            f.write(str(self.publicKey[0]) + "%" + str(self.publicKey[1]) + '\n')
            f.close()
        else:
            for i in range(len(firstIPs)):
                self.p2p.connect_with_node(firstIPs[i], firstPorts[i])
            self.sendData("getAllBlocks") # On récupère toute la chaîne du reste du réseau
            time.sleep(2)
            self.sendData("getHospitals") # On récupère la liste avec les clés
            time.sleep(2)
            self.sendData("getTotalClients") # On récupère le nombre total de client (et donc notre id à nous)
            time.sleep(2)


    def sendData(self, command, params=[]): 
        """Envoie la commande à tout les pairs
        command: str avec la commande
        params: tableau de str avec les parametres"""

        contents = {"command": command, "params":params}

        self.p2p.sendData(contents)
        


    def receivedData(self, contents): 
        # Pour les data, on peut prendre une STR de la forme "command|parametre1/param2/param3..."
        # Les demandes en respond sont potentiellement différentes voir comment gérer les réponses avec une bibliothèque
        
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
            self.sendData("getHospitals")
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
            self.idClient = params[0] + 1
            f = open(self.pathToHopitalList, "a")
            f.write(str(self.publicKey[0]) + "%" + str(self.publicKey[1]) + '\n')
            f.close()
            self.sendData("respondHospitals", [self.getHospitals()])




    def getPerson(self, personId): # Renvoie un objet Person que l'on connait
        for p in self.listPerson:
            if p.personId == personId:
                return p
        return None

    def getUnknownPerson(self, personId):
        self.sendData("getPerson", [personId])

        time.sleep(5)

        return self.getPerson(personId)

    def parseBlock(self, block):
        """Lit les transactions dans un bloc donné et met à jour la liste des personnes"""
        listTrans = block.transactions # Liste des transactions du blocs
        for trans in listTrans:
            persFound = False
            for pers in listPerson:
                if trans.personId == pers.personId:
                    persFound = True
                    malFound = False
                    for mal in pers.medicalHistory:
                        if mal.malId == trans.malId:
                            mal.addDate(trans.newDate)
                            malFound = True
                    if not malFound:
                        mal = Maladie(trans.malId)
                        mal.addDates(trans.newDate)
                        pers.medicalHistory += [mal]
            
                        
            if not persFound:
                pers = getUnknownPerson(trans.personId) # On récupère les infos de la personne du reste du réseau
                if pers != None:
                    malFound = False               
                    for mal in pers.medicalHistory:
                        if mal.malId == trans.malId:
                            malFound = True
                            if trans.newDate not in mal.dates:
                                mal.addDate(trans.newDate)
                    if not malFound:
                       mal = Maladie(trans.malId)
                       mal.addDates(trans.newDate)
                       pers.medicalHistory += [mal]

                    listPerson += [pers]

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
            for i in range(low+1, lenOri):
                f.write(linesOri[i] + '\n')
        else:
            for i in range(low+1, lenNew):
                f.write(linesNew[i] + '\n')

    def sendTrans(self, trans):
        self.sendData("addTransToBlock", [trans.transToString()])

    def getTotalClients(self):
        f = open(self.pathToHopitalList, "r")
        size = len(f.readlines()) - 1
        f.close()
        return size