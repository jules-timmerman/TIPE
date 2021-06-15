class Person:
    
    staticLastPersonId = 0
     
    def __init__(self, name, hospital):
        self.personId = staticLastPersonId
        staticLastId += 1

        self.name = name            
        self.hospital = hospital        # C'est selon ca que l'on saura les clés
        self.medicalHistory = []        # Tableau de Maladie

    
    




