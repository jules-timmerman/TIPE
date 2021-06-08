class Blockchain:
    

    N = 5 # Nombre de transactions par blocs (temporaire)

    def __init__(self):
        self.validBlocks = []        # blocs 100% sûr qui peuvent être pris en compte
        # Contient différentes alternatives de blockchain 
        # On va mettre toutes la blockchain dedans pour faciliter les comparaisons de taille
        self.alternateFollowingChains = [[]]  
        

    def  alreadyInAlternate(self,l) :
        for liste in self.alternateFollowingChains :
            if liste == l :
                return True      
        return False

    def chainUpdate(self) :
        lengthSecond = 0        # Longueur de la 2ème liste la plus longue 
        maxLength = 0
        posFirst = 0
        returnValue = [] # Liste des blocs ayant été modifiés
        for (i,val) in enumerate(self.alternateFollowingChains) :
            if len(val) > maxLength :              # Si une liste est plus longue que celle connue
                posFirst = i                      
                maxLength = len(val)                                    
            elif lengthSecond <= len(val) <= maxLength : # On augmente la valeur de la longeur de la 2ème liste si elle est inférieur à maxLength
                    lengthSecond = len(val)                       # et si la longueur de la 2ème liste est inférieur à len(val)
        if maxLength > (lengthSecond + 5) :       
            returnValue = self.alternateFollowingChains[posFirst][:-5]
            self.validBlocks += returnValue    # On ne rajoute des blocks que lorsqu'on a suffisamment d'éléments par rapport aux autres chaînes et qu'on pas de doublons
            self.alternateFollowingChains = [self.alternateFollowingChains[posFirst][-5:]]
        return returnValue


    def getLastValidBlock(self):
        return self.validBlocks[-1]


    def addBlockToAlternateChain(self,block) :
        pos = block.blockId
        for (i,val) in enumerate(self.alternateFollowingChains) :
            if val[pos-1].hashBlock() == block.lbHash :                             # On ne garde que les chaînes dont l'id du dernier block correspond
                if val[pos: ] != [] :                       
                    self.alternateFollowingChains += [ val[ : pos-1] + [block]]      # S'il existe des éléments après la chaîne que l'on veut compléter on en créer une nouvelle
                else :
                    self.alternateFollowingChains[i] =  ( val[ : pos-1] + [block] )  # Sinon on modifie le block en rajoutant le block d'entrée



    