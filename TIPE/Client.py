from P2P import P2P
import socket
from Blockchain import Blockchain
from Crypto.PublicKey import RSA
from hashlib import sha256


class Client:
    
    refIP = "" # A REMPLIR AVEC LA FUTURE IP DU RASPBERRY EN GROS OU EN TOUT CAS D'UNE ENTITE DE REFERENCE QUI SERA TOUJOURS DANS LA CHAINE
    refPort = -1

    idClient = 0


    def __init__(self, port, firstIPs=[refIP], firstPorts=[refPort]): # firstIPs est un tableau de premiers pairs à qui se connecter idem firstPorts
        self.blockchain = Blockchain()
        self.listPerson = []  
        
        Client.idClient += 1
        self.idClient = Client.idClient
        
        keyPair = RSA.generate(bits=1024)

        self.publicKey =  [keyPair.n, keyPair.e]
        self.privateKey = [keyPair.n, keyPair.d]
        

        self.p2p = P2P(socket.gethostbyname(socket.gethostname()), port, self.receivedData)
        #self.p2p = P2P("127.0.0.1", port, self.receivedData)
        self.p2p.start()

        for i in range(len(firstIPs)):
            self.p2p.connect_with_node(firstIPs[i], firstPorts[i])


    def sendData(self, command, params): 
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

        if command == "getAllBlocks":   # Envoie l'entièreté de la blockchain 
            pass
        elif command == "receiveAllBlocks":   # C'est la commande reçu après avoir fait getAllBlocks (avec donc les blocs)
            pass
        elif command == "getHospitals":
            pass
        elif command == "receiveHospitals":
            pass
        elif command == "newBlock":
            pass



    def getInfoAboutPerson(personId): # Renvoie un objet Person
        # Ca demande des infos au reste du réseau à propos de la personne
        pass


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
                pers = getInfoAboutPerson(trans.personId) # On récupère les infos de la personne du reste du réseau
               
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



