from P2P import P2P
import socket
from Blockchain import Blockchain
from Crypto.PublicKey import RSA
from hashlib import sha256
from Person import Person
import time
from Block import Block


class Client:
    
    refIP = "" # A REMPLIR AVEC LA FUTURE IP DU RASPBERRY EN GROS OU EN TOUT CAS D'UNE ENTITE DE REFERENCE QUI SERA TOUJOURS DANS LA CHAINE
    refPort = -1


    def __init__(self, port, firstIPs=[refIP], firstPorts=[refPort], isFirstClient = False): # firstIPs est un tableau de premiers pairs à qui se connecter idem firstPorts
        self.blockchain = Blockchain()
        self.listPerson = []  

        self.idClient = -1
        
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

            self.blockchain.validBlocks = [Block(0,0, [], 0)]
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


    # CLIENT FUNCTIONS

    def parseBlock(self, block):
        """Lit les transactions dans un bloc donné et met à jour la liste des personnes"""
        listTrans = block.transactions # Liste des transactions du blocs
        for trans in listTrans: # On regarde les transactions du blocs
            persFound = False
            for pers in self.listPerson:
                if trans.personId == pers.personId:
                    persFound = True
                    malFound = False
                    for mal in pers.medicalHistory: # On boucle maintenant sur les maladies que l'on connait 
                        if mal.malId == trans.malId: # Une fois que l'on a trouvé la maladie en question
                            mal.addDate(trans.newDate) # On ajoute la date
                            malFound = True
                    if not malFound: # Si on avait pas trouvé la maladie
                        mal = Maladie(trans.malId) # On crée la maladie
                        mal.addDates(trans.newDate) # Et on ajoute la date
                        pers.medicalHistory += [mal] # Et on ajoute la maladie à l'historique de la personne
            
                        
            if not persFound:
                pers = self.getUnknownPerson(trans.personId) # On récupère les infos de la personne du reste du réseau
                if pers != None:
                    malFound = False               
                    for mal in pers.medicalHistory: # On refait comme avant à la recherche de la maladie
                        if mal.malId == trans.malId:
                            malFound = True
                            if trans.newDate not in mal.dates: # Si la date n'est pas déjà dedans (on a pu recevoir une info déjà mise à jour
                                mal.addDate(trans.newDate)
                    if not malFound: # Si on a pas trouvé la maladie on va la rajouter
                       mal = Maladie(trans.malId)
                       mal.addDates(trans.newDate)
                       pers.medicalHistory += [mal]

                    listPerson += [pers]

    def sendTrans(self, trans):
        self.sendData("addTransToBlock", [trans.transToString()])
