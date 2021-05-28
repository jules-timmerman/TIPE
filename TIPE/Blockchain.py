class Blockchain:
    
    def __init__(self):
        self.validBlocks = []        # blocs 100% sûr qui peuvent être pris en compte
        # Contient différentes alternatives de blockchain 
        # On va mettre toutes la blockchain dedans pour faciliter les comparaisons de taille
        self.alternateFollowingChains = [[]]   