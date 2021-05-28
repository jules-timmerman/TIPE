class Blockchain:
    
    def __init__(self):
        self.validBlocks = []        # blocs 100% sûr qui peuvent être pris en compte
        # Contient différentes alternatives de blockchain 
        # On va mettre toutes la blockchain dedans pour faciliter les comparaisons de taille
        self.alternateFollowingChains = [[]]   
    
    def chainUpdate(self) :
        compteurFirst = 0
        compteurSecond = 0
        maxLength = 0
        pos = 0
        for (i,val) in enumerate(self.alternateFollowingChains) :
            if len(val) > maxLength :
                pos = i 
                compteurFirst = 0
                maxLength = len(val)
            if len(val) == maxLength :
                compteurFirst += 1
                if compteurSecond < len(val) :
                    compteurSecond = len(val)
        if compteurFirst == 0 and compteurFirst > (compteurSecond + 5) :
            self.validBlocks += self.alternateFollowingChains[:-5]




















