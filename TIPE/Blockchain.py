from PySide6.QtCore import QObject, Signal
from Block import Block

class Blockchain(QObject): # On hérite pour GRAPHICS

    N = 5 # Nombre de transactions par blocs (temporaire)
    NAvance = 2 # Nombre de blocs d'avance pour valider

    updateSignal = Signal() # GRAPHICS

    def __init__(self):
        super().__init__() # GRAPHICS

        self.validBlocks = [Block(0 ,0 ,[] ,0)]      # blocs 100% sûr qui peuvent être pris en compte
        # Contient différentes alternatives de blockchain 
        # On va mettre toute la blockchain dedans pour faciliter les comparaisons de taille
        self.alternateFollowingChains = [[Block(0 ,0 ,[] ,0)]]  


    def alreadyInAlternate(self,l) :
        for liste in self.alternateFollowingChains :
            if liste == l :
                return True      
        return False

    # Met à jour valid et vide alternate si suffisament d'avance
    def chainUpdate(self) :
        lengthSecond = 0        # Longueur de la 2ème liste la plus longue 
        maxLength = 0
        posFirst = 0
        returnValue = [] # Liste des blocs ayant été modifiés
        for (i,val) in enumerate(self.alternateFollowingChains) :
            if len(val) > maxLength :              # Si une liste est plus longue que celle connue
                posFirst = i
                lengthSecond = maxLength
                maxLength = len(val)                                    
            elif lengthSecond <= len(val): # On augmente la valeur de la longeur de la 2ème liste si elle est inférieur à maxLength
                lengthSecond = len(val)                       # et si la longueur de la 2ème liste est inférieur à len(val)
        
        if maxLength > (lengthSecond + Blockchain.NAvance) : 
            print("UPDATING CHAIN\n")
            returnValue = self.alternateFollowingChains[posFirst][:-Blockchain.NAvance] # On va chercher tout les blocs sauf les derniers d'avances

            self.validBlocks = returnValue    # On ne rajoute des blocks que lorsqu'on a suffisamment d'éléments par rapport aux autres chaînes et qu'on pas de doublons
            self.alternateFollowingChains = [self.alternateFollowingChains[posFirst]] # On vide les alternates
        
        self.updateSignal.emit() # GRAPHICS

        return returnValue # Renvoie ce qui a été rajouté


    def getLastValidBlock(self):
        return self.validBlocks[-1]


    def addBlockToAlternateChain(self,block) :
        Id = block.blockId
        if Id != 0 : # Juste pas le bloc origine
            for (i,val) in enumerate(self.alternateFollowingChains) : # On regarde chacune des potentielles chaînes
                if len(val) > (Id-1) : # La potentielle est plus longue que l'id du bloc (donc le bloc est à l'intérieur et pas dans le vide après)
                    if (val[Id-1]).hashBlock() == block.lbHash: # La pot possède un block pouvant être avant notre bloc
                        if val[Id:] == [] : # S'il n'y a rien après (on est donc en bout de chaîne)
                            self.alternateFollowingChains[i] = val + [block] # On rajoute juste le block à la pot
                        elif val[Id] != block: # Il y avait des choses après notre bloc, on vérifie que c'est différent pour éviter de boucler à l'infini
                            self.alternateFollowingChains += [val[:Id] + [block]] # On crée une nouvelle chaîne pot

    def addBlocksToAlternateChain(self, blocks):
        for b in blocks:
            self.addBlockToAlternateChain(b)
    
    @staticmethod
    def blocksToString(blocks): # Méthode générale de conversion
        resStr = ""

        for b in blocks:
            strBlock = b.blockToString()
            resStr += strBlock
            resStr +=  "!"
        resStr = resStr[:-1]

        return resStr

    def validBlocksToString(self) : 
        return Blockchain.blocksToString(self.validBlocks)

    def alternateFollowingChainsToString(self) :
        resStr = ""
        for chain in self.alternateFollowingChains :
            resStr += Blockchain.blocksToString(chain)
            resStr += "£" # Sep les pots
        resStr = resStr[:-1]

        return resStr
    @staticmethod
    def stringToAlternateFollowingChains(string) :
        res1 = []
        
        split1 = string.split("£")
        
        for chain in split1 :
            c = Blockchain.stringToBlocks(chain)
            res1 += [c]
        
        return res1

    def blockchainToString(self) :
        resStr = ""

        resStr += self.alternateFollowingChainsToString()

        resStr += "µ"

        resStr += self.validBlocksToString()

        return resStr

    @staticmethod
    def stringToBlocks(string):
        aux = string.split("!")
        blocks = []
        
        for block in aux :
            blocks += [Block.stringToBlock(block)]

        return blocks

    @staticmethod
    def stringToValidBlocks(string) :
        return Blockchain.stringToBlocks(string)

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


