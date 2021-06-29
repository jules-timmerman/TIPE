from os import chdir as ch 

class Maladie:

    def __init__(self, malId):
        self.malId = malId
        self.nom = Maladie.getMalName(id)
        self.dates = [] # Chaines de caractères au format JJ/MM/AAAA

    def isInfected(self): 
        return len(self.dates) % 2 == 0

    def addDate(self,date):
        self.dates += [date]
    
    @staticmethod
    def getMalName(id) :
        f = open ('listeMaladie.txt' , 'r')
        w = f.readLines()
        f.close()
        if id >= len(w): # Pas trouvé
            return ""
        return w[id]

    def getMalId (nomMal) :
        f = open ('listeMaladie.txt' , 'r')
        w = f.readLines()
        for (k, val) in enumerate(w) :
            if val + "\n" == nomMal :
                f.close()
                return k
        f.close()
        return -1 # Pas trouvé 

    def maladieToString(self):
        s = ""
        s += str(self.malId) + "|"
        s += self.nom + "|"
        for d in self.dates:
            s += d + "$"
        return s[:-1]


    @staticmethod
    def stringToMaladie(s):
        t = s.split("|")
        mal = Maladie(int(t[0]))
        mal.nom = t[1]
        mal.dates = t[2].split("$")
        