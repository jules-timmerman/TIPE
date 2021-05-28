class Person:
    
    staticLastPersonId = 0
     
    def __init__(self, name, dob, hospital):
        self.personId = staticLastPersonId
        staticLastId += 1

        self.name = name
        self.dob = dob
        self.hospital = hospital
        self.medicalHistory = []        # Tableau de maladie j'imagine ?

    
    




