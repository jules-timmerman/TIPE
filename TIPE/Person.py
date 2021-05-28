class Person:
    
    staticLastPersonId = 0
     
    def __init__(self, name, dob, hospital):
        self.personId = staticLastPersonId
        staticLastId += 1

        self.name = name
        self.dob = dob                  # str format JJ/MM/AAAA
        self.hospital = hospital        # C'est selon ca que l'on saura les clés
        self.medicalHistory = []        # Tableau de maladie j'imagine ?

    
    




