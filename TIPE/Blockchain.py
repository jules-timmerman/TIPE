class Blockchain:
    
    def __init__(self):
        self.validBlocks = []        # blocs 100% sûr qui peuvent être pris en compte
        # Contient différentes alternatives de blockchain 
        # On va mettre toutes la blockchain dedans pour faciliter les comparaisons de taille
        self.alternateFollowingChains = [[]]   

    def  alreadyInAlternate(self,l) :
        for liste in self.alternateFollowingChains :
            if liste == l :
                return True
        else :          
            return False

    def chainUpdate(self) :
        compteur = 0            # Compteur du nombre de liste ayant la même longeur que la liste la plus longue
        lengthSecond = 0        # Longueur de la 2ème liste la plus longue 
        maxLength = 0
        posFirst = 0
        for (i,val) in enumerate(self.alternateFollowingChains) :
            if len(val) > maxLength :              # Si une liste est plus longue que celle connue
                posFirst = i                      
                compteur = 0                       # On reset le compteur du nombre de la liste de même longeur que la plus longue 
                maxLength = len(val)                
            if len(val) == maxLength :
                compteur += 1                       
            if len(val) < maxLength and lengthSecond < len(val) : # On augmente la valeur de la longeur de la 2ème liste si elle est inférieur à maxLength
                    lengthSecond = len(val)                       # et si la longueur de la 2ème liste est inférieur à len(val)
        if compteur == 0 and maxLength > (lengthSecond + 5) :       
            self.validBlocks += self.alternateFollowingChains[posFirst][:-5]    #On ne rajoute des blocks que lorsqu'on a suffisamment d'éléments par rapport aux autres chaînes et on pas de doublons




















