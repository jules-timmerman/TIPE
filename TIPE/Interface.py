from PySide6.QtWidgets import *
from MCListWidgetItem import MCListWidgetItem
from BlockchainHUD import BlockchainGraphics
from MCChainWidget import MCChainWidget
from Blockchain import Blockchain

from Simulation import Simulation
import threading

class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self._mainLayout = QHBoxLayout()

        self._mainMenuWidget = QWidget(self)
        self._mainMenuWidgetLayout = QGridLayout()

        self._etatWidget = QWidget(self)
        self._etatWidgetLayout = QGridLayout()
        self._etatWidget.hide()

        self._mcChainWidget = MCChainWidget(Blockchain())
        self._mcChainWidget.hide()

        ## Mise en place du Main Widget
        self._buttonTransaction = QPushButton("Generer une transaction", self)
        self._buttonMineur = QPushButton("Generer un mineur", self)
        self._buttonClient = QPushButton("Generer un client", self)
        self._buttonEtat = QPushButton("Etat du systeme", self)
        self._buttonSimulation = QPushButton("Simulation", self)
        self._buttonPause = QPushButton("Pause", self)

        self._buttonTransaction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonMineur.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonClient.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonEtat.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonSimulation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonPause.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self._buttonTransaction.clicked.connect(self.genTransaction)
        
        #self._buttonMineur.clicked.connect(self.threadGenMineur)
        #self._buttonClient.clicked.connect(self.threadGenClient)
        
        self._buttonMineur.clicked.connect(self.genMineur)
        self._buttonClient.clicked.connect(self.genClient)

        self._buttonEtat.clicked.connect(self.etat)
        self._buttonSimulation.clicked.connect(self.simulate)
        self._buttonPause.clicked.connect(self.pause)

        self._mainMenuWidgetLayout.addWidget(self._buttonTransaction, 0, 0)
        self._mainMenuWidgetLayout.addWidget(self._buttonMineur, 0, 1)
        self._mainMenuWidgetLayout.addWidget(self._buttonClient, 1, 0)
        self._mainMenuWidgetLayout.addWidget(self._buttonEtat, 1, 1)
        self._mainMenuWidgetLayout.addWidget(self._buttonSimulation, 2, 0)
        self._mainMenuWidgetLayout.addWidget(self._buttonPause, 2, 1)

        ## **********************************
        ## Mise en place du (test) etatWidget

        self._listWidgetClient = QListWidget(self)
        self._listWidgetMineur = QListWidget(self)
        self._buttonRetour = QPushButton("Retour")

        self._buttonRetour.clicked.connect(self.retour)
        self._listWidgetClient.itemDoubleClicked.connect(self.showMCChain)
        self._listWidgetMineur.itemDoubleClicked.connect(self.showMCChain)


        self._etatWidgetLayout.addWidget(self._listWidgetClient, 0, 0)
        self._etatWidgetLayout.addWidget(self._listWidgetMineur, 0, 1)
        self._etatWidgetLayout.addWidget(self._buttonRetour, 1, 0, 1, 2)

        ## **********************************

        self._mainLayout.addWidget(self._mainMenuWidget)


        ## On set tout les Layouts
        self._mainMenuWidget.setLayout(self._mainMenuWidgetLayout)
        self._etatWidget.setLayout(self._etatWidgetLayout)
        self.setLayout(self._mainLayout)

        self.setWindowTitle("Blockchain TIPE")

        ## ***************************************
        ## ** FIN DE LA CREATION DE L'INTERFACE **
        ## ***************************************

        ## POUR LA SIMULATION

        self.simulation = Simulation()
        MCListWidgetItem(self.simulation.clients[0], str(self.simulation.clients[0].p2p.port) + " : " + str(self.simulation.clients[0].idClient), self._listWidgetClient)
        MCListWidgetItem(self.simulation.miners[0], str(self.simulation.miners[0].p2p.port), self._listWidgetMineur)


    def genTransaction(self): 
        self.simulation.createRandomTrans()


    def genMineur(self): # A mettre dans un Thread pour ne pas bloquer l'interface
        m = self.simulation.createMiner()
        MCListWidgetItem(m, str(m.p2p.port), self._listWidgetMineur)

    def threadGenMineur(self): # La version dans un thread
        t = threading.Thread(target = self.genMineur, daemon = True)
        t.start()

    def genClient(self): # A mettre dans un Thread pour ne pas bloquer l'interface
        c = self.simulation.createClient()
        MCListWidgetItem(c, str(c.p2p.port) + " : " + str(c.idClient), self._listWidgetClient)

    def threadGenClient(self): # La version dans un thread
        t = threading.Thread(target = self.genClient, daemon = True)
        t.start()


    def etat(self):
        self._mainLayout.replaceWidget(self._mainMenuWidget, self._etatWidget)
        self._etatWidget.show()
        self._mainMenuWidget.hide()


    def showMCChain(self, item: MCListWidgetItem):
        self._mcChainWidget.changeBlockchain(item.mc.blockchain)
        self._mcChainWidget.show()
    

    def simulate(self):
        pass

    def pause(self):
        pass

    def retour(self):
        self._mainLayout.replaceWidget(self._etatWidget, self._mainMenuWidget)
        self._mainMenuWidget.show()
        self._etatWidget.hide()












