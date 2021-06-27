class Miner:

    from hashlib import sha256


    def __init__(self):
        self.blockchain = Blockchain()
        self.transToBlock = []      # Liste de transactions à ajouter 
        # Lancer ici un Thread avec une fonction qui va écouter le réseau et une fonction de callback (ici receivedData) 
        # CF Asyncio
        # Gérer les connaissances des autres nodes




    def receivedData(content):  
        # Pour les data, on peut prendre une STR de la forme "command|parametre1/param2/param3..."
        # Les demandes en respond sont potentiellement différentes voir comment gérer les réponses avec une bibliothèque
        t = content.split("|")
        command = t[0]
        params = t[1].split("/")

        if command == "getAllBlocks":   # Envoie l'entièreté de la blockchain au param1 
            sendAllBlock(params[0])  
        elif command == "respondAllBlocks":   # C'est la commande reçu après avoir fait getAllBlocks
            pass
        elif command == "getHospitals":
            pass
        elif command == "respondHospitals":
            pass
        elif command == "newBlock":
            pass


        elif command == "blockTrans":
            pass


    def addTransToBlock(self, trans):
        self.transToBlock += trans
        if len(transToBlock >= 5):
            self.block() # Peut-être mettre dans un Thread plutôt 

    def sendAllBlock(ip): # Envoie à l'ip passé en parametre (en str)

        pass

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
        self.sendBlock(blockTemp)

    def sendBlock(self, blockTemp): # Envoie le bloc au reste de réseau (A FAIRE PLUS TARD)
        pass
    
    def receivedTrans(self,senderId,transaction) :
        signature = transaction.signature
        f = open("listeHopital.txt")
        publicKey = f[senderId]

        s = ""
        s += str(transaction.personId) + "|"
        s += str(transaction.maladieId) + "|"
        s += str(transaction.newDate) + "|"
        s += str(transaction.clientId) 
        
        hash = int.from_bytes(sha256(s).digest(), byteorder='big')
            
        hashFromSignature = pow(signature, publicKey[1], publicKey [0])
 
        if hashFromSignature == hash :
            addTransToBlock(self,transaction) 

