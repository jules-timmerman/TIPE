import Transaction
import hashlib


def hash(sum, pow): # Sum en str et pow un nombre
     return hashlib.sha256((sum + str(pow)).encode("utf-8"))


class Block:

    NZeros = 7 # Nombre de zéros à mettre pour la PoW


    def __init__(self, blockId, lbHash, transactions, proofOfWork = 0,__sumTemp__ = 0):
        self.blockId = blockId  # Id du bloc pour avoir une idée de l'ordre
        self.lbHash = lbHash    # Hash du dernier bloc
        self.proofOfWork = proofOfWork    # Proof of work du hash
        self.transactions = transactions  # Liste de Transaction
        self.__sumTemp__ = self.__sum__() # Somme temporaire de tous les attributs sauf proof of work
    
    def __sum__(self):
        toHash = ""
        toHash += str(self.blockId)
        toHash += str(self.lbHash)
        for v in self.transactions:
            toHash += v.toString()
        self.__sumTemp__ = toHash

    def hashBlock(self): # Calcul le hash d'un bloc
        return hash(self.__sumTemp__, self.proofOfWork)

    def hashBlockWithPOW(self, pow):
        return hash(self.__sumTemp__, pow)

    def blockToString (self):
        # Caractéristiques du blocs séparé par des /
        # Les différentes transactions par des @
        resStr = ""
        resStr += str(self.blockId) + "/"
        resStr += str(self.lbHash) + "/"
        resStr += str(self.proofOfWork) + "/"

        for trans in self.transactions :
            aux = trans.transToString()
            resStr += aux + '@'
        resStr = resStr[:-1] 
            
        return resStr

    @staticmethod   
    def stringToBlock (string) :
        aux1 = string.split("/")
        blockId = aux1[0]
        lbHash = aux1[1]
        proofOfWork = aux1[2]

        transactions = []
        aux2 = (aux1[3]).split("@")
        for trans in aux2 :
            transactions += [Transaction.stringToTrans(trans)]

        block = Block(blockId, lbHash, transactions, proofOfWork)
        return block

    def isValidBlock(self) :
        if self.blockId == 0 :
            return True
        if self.hashBlock()[0:Block.NZeros] != "0" * Block.NZeros:
            for trans in self.transactions :
                if not trans.isValidTrans() :
                    return False
            return True
        return False






