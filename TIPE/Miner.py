class Miner:
    
    def __init__(self):
        self.blockchain = Blockchain()
        self.transToBlock = []      # Liste de transactions à ajouter 

    def addTransToBlock(self, trans):
        self.transToBlock += trans
        if len(transToBlock >= 5):
            self.block() # Peut-être mettre dans un Thread plutôt 


    def block(self): 
        lb = self.blockchain.getLastValidBlock() # Last Block
        blockId = lb.blockId + 1
        lbHash = lb.hashBlock()
        trans = self.transToBlock[0:5]
        
        blockTemp = Block(blockId, lbHash, trans)

        hashTemp = blockTemp.hashBlock()
        i = 0
        while hashTemp[0:Block.NZeros] != "0" * Block.NZeros:
            i += 1
            hashTemp = blockTemp.hashBlockWithPOW(i)
        blockTemp.proofOfWork = i

        # Il faut envoyer le bloc aled
        self.send(blockTemp)

    def send(self, blockTemp): # Envoie le bloc au reste de réseau
        pass