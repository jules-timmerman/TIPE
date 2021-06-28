from hashlib import sha256

class Transaction:
    

    def __init__(self, personId, maladieId, newDate, clientId,signature = -1):
        self.personId = personId    # id de la personne liée à la transaction
        self.maladieId = maladieId  # id de la maladie liée à la transaction
        self.newDate = newDate      # date à ajouter à la personne (que ce soit attrapée ou perdue)
        self.clientId = clientId    # nom de la personne qui a envoye la transaction
        
        if signature == -1 :
            s = ""
            s += str(self.personId) + "|"
            s += str(self.maladieId) + "|"
            s += str(self.newDate) + "|"
            s += str(self.clientId) 
            signature = int.from_bytes(sha256(s).digest(), byteorder='big')
            self.signature = signature  # Signature de la transaction
                                    # Ici par l'hopital et donc fait avec la clé privée
        
    
    def transToString(self): # Séparateurs entre infos d'une transaction sont |
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.signature) + "|"
        s += str(self.clientId) 
        return s

    def stringToTrans (string) :
        aux = string.split("|")
        personId = aux[0]
        maladieId = aux[1]
        newDate = aux[2]
        signature = aux[3]
        clientId = aux[4]
        
        transaction = Transaction(personId, maladieId, newDate, clientId,signature)
        
        return transaction 
    
    def isValidTrans(self) :
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.signature) + "|"
        s += str(self.clientId) 

        signature = int.from_bytes(sha256(s).digest(), byteorder='big')

        if self.signature == signature :
            return True
        return False
