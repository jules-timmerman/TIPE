class Maladie:

    def __init__(self, malId):
        self.malId = malId
        self.nom = ""
        self.dates = [] # Chaines de caractères au format JJ/MM/AAAA

    def isInfected(self): 
        return len(self.dates) % 2 == 0

    def addDate(date):
        dates += date
