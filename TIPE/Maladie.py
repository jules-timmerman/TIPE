from os import chdir as ch 

class Maladie:

    def __init__(self, malId):
        self.malId = malId
        self.nom = ""
        self.dates = [] # Chaines de caractères au format JJ/MM/AAAA

    def isInfected(self): 
        return len(self.dates) % 2 == 0

    def addDate(date):
        dates += [date]

    def getMalName(id) :
        f = open ('listeMaladie.txt' , 'r')
        w = f.readLines()
        f.close()
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