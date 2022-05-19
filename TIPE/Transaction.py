from hashlib import sha256
from pathlib import Path
import random as rd


class Transaction:
    

    def __init__(self, personId, maladieId, newDate, clientId, privateKey = - 1):
        self.personId = personId    # id de la personne liée à la transaction
        self.maladieId = maladieId  # id de la maladie liée à la transaction
        self.newDate = newDate      # date à ajouter à la personne (que ce soit attrapée ou perdue)
        self.clientId = clientId    # nom de la personne qui a envoye la transaction
        
        self.signature = -1

        if privateKey != -1:
            s = ""
            s += str(self.personId) + "|"
            s += str(self.maladieId) + "|"
            s += str(self.newDate) + "|"
            s += str(self.clientId) 
            
            hash = int.from_bytes(sha256(bytes(s, 'utf-8')).digest(), byteorder='big')
        
            hashSignature = pow(hash, privateKey[1], privateKey[0])

            self.signature = hashSignature  # Signature de la transaction
                                            # Ici par l'hopital et donc fait avec la clé privée
        
    
    def __eq__(self, other):
        return self.personId == other.personId and self.maladieId == other.maladieId and self.newDate == other.newDate and self.clientId == other.clientId and self.signature == other.signature


    def transToString(self): # Séparateurs entre infos d'une transaction sont |
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.signature) + "|"
        s += str(self.clientId) 
        return s

    @staticmethod
    def stringToTrans (string) :
        aux = string.split("|")
        personId = int(aux[0])
        maladieId = int(aux[1])
        newDate = aux[2]
        signature = int(aux[3])
        clientId = int(aux[4])
        
        transaction = Transaction(personId, maladieId, newDate, clientId)
        transaction.signature = signature
        
        return transaction 
    
    def isValidTrans(self) :
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.clientId) 

        p = Path('.')
        hopitalFile = None

        f = open("listeHopital8000.txt", "r") # TODO : essayer de trouver un fichier pour sûr
        g = f.readlines()
        h = g[self.clientId].split("%")

        hash = int.from_bytes(sha256(bytes(s, 'utf-8')).digest(), byteorder='big')
        hashFromSignature = pow(self.signature, int(h[1]),int(h[0]))

        f.close()

        if hashFromSignature == hash :
            return True
        return False

    #@staticmethod
    #def randTransOLD(nbPatients,nbMaladies,idClient):
        
    #    idPatient = rd.randint(0,nbPatients)
    #    idMaladie = rd.randint(0,nbMaladies)
        
    #    jour = rd.randint(0,31)
    #    annee = rd.randint(1980,2031)
    #    mois = rd.randint(0,13)
    #    strDate = str(jour) + "/" + str(mois) + "/" + str(annee)
        
    #    keyPair = RSA.generate(bits=1024) # EH ?
    #    clePrivee = [keyPair.n , keyPair.d]

    #    return  Transaction(idPatient, idMaladie, strDate, idClient, clePrivee)

    @staticmethod
    def randomTrans(clients, maxPersonId = 100, maxMaladieId = 20, minAnnee = 1970, maxAnnee = 2030):
        personId = rd.randint(0,maxPersonId)
        maladieId = rd.randint(0,maxMaladieId)
        jour = rd.randint(0,31) # Aller c'est pas grave y'aura un 31 fevrier
        mois = rd.randint(0,12)
        annee = rd.randint(minAnnee, maxAnnee)
        newDate = str(jour) + ";" + str(mois) + ";" + str(annee)
        clientIndex = rd.randint(0,len(clients) - 1) # C'est inclu donc pas de OOR
        client = clients[clientIndex]
        return Transaction(personId, maladieId, newDate, client.idClient, client.privateKey)






