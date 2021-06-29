from hashlib import sha256

class Transaction:
    

    def __init__(self, personId, maladieId, newDate, clientId,privateKey):
        self.personId = personId    # id de la personne liée à la transaction
        self.maladieId = maladieId  # id de la maladie liée à la transaction
        self.newDate = newDate      # date à ajouter à la personne (que ce soit attrapée ou perdue)
        self.clientId = clientId    # nom de la personne qui a envoye la transaction
        
        
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.clientId) 
            
        hash = int.from_bytes(sha256(bytes(s, 'utf-8')).digest(), byteorder='big')
        
        signature = pow(hash, privateKey[1], privateKey[0])

        self.signature = signature  # Signature de la transaction
                                    # Ici par l'hopital et donc fait avec la clé privée
        
    
    def transToString(self): # Séparateurs entre infos d'une transaction sont |
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.signature[0]) + "%" + str(self.signature[1]) + "|"
        s += str(self.clientId) 
        return s

    @staticmethod
    def stringToTrans (string) :
        aux = string.split("|")
        personId = int(aux[0])
        maladieId = int(aux[1])
        newDate = aux[2]
        
        aux2 = aux[3].split("%")
        signature = [int(aux2[0]),int(aux2[1])]
        clientId = int(aux[4])
        
        transaction = Transaction(personId, maladieId, newDate, clientId,signature)
        
        return transaction 
    
    def isValidTrans(self) :
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.clientId) 

        f = open("listeHopital.txt", "r")
        g = f.readlines()
        h = g[self.clientId].split("%")

        hash = int.from_bytes(sha256(bytes(s, 'utf-8')).digest(), byteorder='big')
        hashFromSignature = pow(self.signature, int(h[1]),int(h[0]))

        f.close()

        if hashFromSignature == hash :

            return True
        return False
