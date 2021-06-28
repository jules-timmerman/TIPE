import Maladie

class Person:
    
    staticLastPersonId = 0
     
    def __init__(self, name, hospital):
        self.personId = Person.staticLastPersonId
        Person.staticLastPersonId += 1

        self.name = name            
        self.medicalHistory = []        # Tableau de Maladie

    
