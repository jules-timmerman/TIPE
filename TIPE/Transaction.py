class Transaction:


    def __init__(self, personId, maladieId, newDate, clientId, signature):
        self.personId = personId    # id de la personne liée à la transaction
        self.maladieId = maladieId  # id de la maladie liée à la transaction
        self.newDate = newDate      # date à ajouter à la personne (que ce soit attrapée ou perdue)
        self.signature = signature  # Signature de la transaction
                                    # Ici par l'hopital et donc fait avec la clé privées
        self.clientId = clientId
    
    def transToString(self):
        s = ""
        s += str(self.personId) + "/"
        s += str(self.maladieId) + "/"
        s += str(self.newDate) + "/"
        s += str(self.signature) + "/"
        s += str(self.clientId) 
        return s