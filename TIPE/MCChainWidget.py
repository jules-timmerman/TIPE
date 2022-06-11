from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QWidget, QHBoxLayout

from Blockchain import Blockchain
from BlockchainHUD import BlockchainGraphics


class MCChainWidget(QWidget): # MC : Miner / Client (marche pour les deux)
    # Il s'agit de la fenêtre affichant la chaîne qui apparait en double cliquant
    
    def __init__(self, blockchain: Blockchain, parent: QWidget = None):
        super().__init__(parent)

        self.layout = QHBoxLayout()

        self.scene = QGraphicsScene(self)
        
        self.blockchain = blockchain
        self.blockchainGraphics = BlockchainGraphics(self.blockchain, self.scene)
        self.scene.addItem(self.blockchainGraphics)

        self.view = QGraphicsView(self.scene, self)
        
        
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

    def changeBlockchain(self, bc):
        self.blockchain = bc
        self.blockchainGraphics.blockchain = bc
        # On nettoie à la main alternate avant :
        for g in self.blockchainGraphics.alternateBlockGraphss:
            self.blockchainGraphics.deleteGraphs(g)

        self.blockchainGraphics.graphsFromValid()
        self.blockchainGraphics.graphsFromAlternate()
    





