from Client import Client
from Miner import Miner
from Transaction import Transaction

class Simulation:

    def __init__(self, clientStartPort = 8000, minerStartPort = 9000, refIPs = ["127.0.0.1"], refPorts = [8000]):
        self.clientStartPort = clientStartPort
        self.minerStartPort = minerStartPort
        self.refIPs = refIPs ; self.refPorts = refPorts
        self.clients = [Client(clientStartPort, isFirstClient = True)] 
        self.miners = [Miner(minerStartPort, refIPs, refPorts)]

    def createClient(self): # Renvoie le client cree (si besoin)
        c = Client(self.clientStartPort + len(self.clients), self.refIPs, self.refPorts)
        self.clients += [c]
        return c

    def createMiner(self): # Renvoie le mineur cree (si besoin)
        m = Miner(self.minerStartPort + len(self.miners), self.refIPs, self.refPorts)
        self.miners += [m]
        return m

    def createRandomTrans(self): # Cree et envoie une transaction generee au hasard (et renvoie si besoin)
        trans = Transaction.randomTrans(self.clients)
        self.clients[trans.clientId].sendTrans(trans)
        return trans



