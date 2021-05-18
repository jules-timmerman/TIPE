class Block:

    # Relire / revoir comment faire un block 
    # Il va falloir des trucs genre les signatures, qui a miné, les hashs

    def __init__(self, blockId, lbHash):
        self.blockId = blockId
        self.lbHash = lbHash
        self.proofOfWork = 0
        self.transactions = []
    

    def addTransaction(trans):
        transactions += trans
        