from Block import Block

class Blockchain:
    

    N = 5 # Nombre de transactions par blocs (temporaire)
    NAvance = 2 # Nombre de blocs d'avance pour valider

    def __init__(self):
        self.validBlocks = [Block(0 ,0 ,[] ,0)]      # blocs 100% sûr qui peuvent être pris en compte
        # Contient différentes alternatives de blockchain 
        # On va mettre toutes la blockchain dedans pour faciliter les comparaisons de taille
        self.alternateFollowingChains = [[Block(0 ,0 ,[] ,0)]]  
        

    def alreadyInAlternate(self,l) :
        if len(l) == 1:
            return True
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
        
        if maxLength > (lengthSecond + Blockchain.NAvance) : 
            print("UPDATING CHAIN\n")
            returnValue = self.alternateFollowingChains[posFirst][:-Blockchain.NAvance] # On va chercher tout les blocs sauf les derniers d'avances

            self.validBlocks = returnValue    # On ne rajoute des blocks que lorsqu'on a suffisamment d'éléments par rapport aux autres chaînes et qu'on pas de doublons
            self.alternateFollowingChains = [self.alternateFollowingChains[posFirst]]
            
        return returnValue # Renvoie ce qui a été rajouté


    def getLastValidBlock(self):
        return self.validBlocks[-1]


    def addBlockToAlternateChain(self,block) :
        Id = block.blockId
        if Id != 0 :
            for (i,val) in enumerate(self.alternateFollowingChains) :
                if len(val) > (Id-1) :
                    if (val[Id-1]).hashBlock() == block.lbHash :
                        if val[Id:] == [] :
                            self.alternateFollowingChains[i] = val + [block]
                        else :
                            self.alternateFollowingChains += [val[:Id] + [block]]


    def validBlocksToString(self) : 
        validBlocks = self.validBlocks
        
        resStr = ""

        for block in validBlocks :    
            strBlock = block.blockToString()
            resStr += strBlock
            resStr += "!" 
        resStr = resStr[:-1]

        return resStr

    def alternateFollowingChainsToString(self) :

        alternateFollowingChains = self.alternateFollowingChains
        resStr = ""

        for chain in alternateFollowingChains :
            for block in chain :
                strBlock = block.blockToString()
                resStr += strBlock
                resStr += "£"
            resStr= resStr[:-1]
            resStr = "#" 
        resStr = resStr[:-1]
        
        return resStr

    @staticmethod
    def stringToAlternateFollowingChains(string) :
        res1 = []
        
        split1 = string.split("#")
        
        for chain in split1 :
            split2 = chain.split("£")
            
            for strBlock in split2 :
                aux = Block.stringToBlock(strBlock)
                res2 = res2 + [aux]

            res1 += [res2]
        
        return res1

    def blockchainToString(self) :
        resStr = ""

        resStr += self.alternateFollowingChainsToString()

        resStr += "µ"

        resStr += self.validBlocksToString()

        return resStr

    @staticmethod
    def stringToBlockchain(string) :

        split = string.split("µ")

        alternateFollowingChains = Blockchain.stringToAlternateFollowingChains(split[0])

        valibBlocks = Blockchain.stringToValidBlocks(split[1])

        blockchain = Blockchain()

        blockchain.alternateFollowingChains = alternateFollowingChains
        blockchain.validBlocks = valibBlocks
        
        return blockchain

    @staticmethod
    def stringToValidBlocks(string) :
        aux = string.split("!")
        validBlocks = []
        
        for block in aux :
            validBlocks += [Block.stringToBlock(block)]

        return validBlocks

    def printBlockchainAndAll(self):
        print("alternate")

        for bcs in self.alternateFollowingChains:
            for b in bcs:
                print(b.blockToString())
            print("--------------")

        print("\n\n")
        print("valid")

        for b in self.validBlocks:
            print(b.blockToString())


