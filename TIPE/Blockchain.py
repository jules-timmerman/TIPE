class Blockchain:
    
    def __init__(self):
        self.validBlocks = []        # blocs 100% sûr qui peuvent être pris en compte
        # Contient différentes alternatives de blockchain 
        # On va mettre toutes la blockchain dedans pour faciliter les comparaisons de taille
        self.alternateFollowingChains = [[]]   
    
    def chainUpdate(self) :
        compteur = 0
        lengthSecond = 0
        maxLength = 0
        posFirst = 0
        for (i,val) in enumerate(self.alternateFollowingChains) :
            if len(val) > maxLength :
                posFirst = i 
                compteur = 0
                maxLength = len(val)
            if len(val) == maxLength :
                compteur += 1
            if len(val) < maxLength and lengthSecond < len(val) :
                    lengthSecond = len(val)
        if compteur == 0 and maxLength > (lengthSecond + 5) :
            self.validBlocks += self.alternateFollowingChains[posFirst][:-5]




















