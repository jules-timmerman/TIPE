class Blockchain:
    validBlocks = []
    alternateFollowingChains = [[]] # Contain different potential sequence of the current valid chain (the longest wins)
     
    def __init__(self):
        self.validBlocks = []
        self.alternateFollowingChains = [[]]

    def lastReceivedBlock(self, block):
        # TODO :
        # Verifier le hash
        # Si pending a un certains nombre d'éléments, on valide les plus vieux et on raccourci la liste
        # (Ou sinon on le fait avec un thread et une clock)
        # On regarde l'id et on compare avec le hash :
        # Si l'id est un dans les blocs valides si le hash est pas bon alors on rejette
        # Si l'id est un des pending on crée une disjonction (si le hash coincide avec l'avant de la chaine)
        pass