class Block:


    def __init__(self, blockId, lbHash):
        self.blockId = blockId  # Id du bloc pour avoir une idée de l'ordre
        self.lbHash = lbHash    # Hash du dernier bloc
        self.proofOfWork = 0    # Proof of work du hash
        self.transactions = []  # Liste de Transaction
    

    def addTransaction(trans):
        transactions += trans
        