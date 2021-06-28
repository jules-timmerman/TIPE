from Maladie import Maladie

class Person:
    
     
    def __init__(self, id, name):
        self.personId = id
        self.name = name            
        self.medicalHistory = []        # Tableau de Maladie


    def personToString(self):
        s = ""
        s += str(self.personId) + "/"
        s += self.name + "/"
        for val in medicalHistory:
            s += val.maladieToString() + "!"
        return s[:-1]

    @staticmethod
    def stringToPerson(s):
        t = s.split("/")
        p = Person(int(t[0]), t[1])
        for malStr in t[2].split("!"):
            self.medicalHistory += Maladie.stringToMaladie(malStr)
    
