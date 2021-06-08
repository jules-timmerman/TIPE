class Client:

    def __init__(self):
        self.blockchain = Blockchain()
        self.listPerson = []            # Liste de Person

    def getAllChain(): # Ask peers for all the chain and compare using alternateFollowingChains
        pass # cf P2P

    def parseBlock(self, block):
        listTrans = block.transactions # Liste des transactions du blocs