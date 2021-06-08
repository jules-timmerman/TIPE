import hashlib


def hash(sum, pow): # Sum en str et pow un nombre
     return hashlib.sha256((sum + str(pow)).encode("utf-8"))


class Block:

    NZeros = 7 # Nombre de zéros à mettre pour la PoW

    def __init__(self, blockId, lbHash, transaction, proofOfWork = 0):
        self.blockId = blockId  # Id du bloc pour avoir une idée de l'ordre
        self.lbHash = lbHash    # Hash du dernier bloc
        self.proofOfWork = proofOfWork    # Proof of work du hash
        self.transactions = transaction  # Liste de Transaction
        self.__sumTemp__ = __sum__() # Somme temporaire de tous les attributs sauf proof of work
    
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