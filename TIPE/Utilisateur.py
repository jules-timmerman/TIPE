from Client import Client
from Miner import Miner

class Utilisateur:

    refIP = "" # A REMPLIR AVEC LA FUTURE IP DU RASPBERRY EN GROS OU EN TOUT CAS D'UNE ENTITE DE REFERENCE QUI SERA TOUJOURS DANS LA CHAINE
    refPort = -1

    def __init__(self, port, firstIPs=[refIP], firstPorts=[refPort]):
        self.client = Client(port, firstIPs, firstPorts)

        