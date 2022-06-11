from PySide6.QtCore import QRectF, Slot, Qt
from PySide6.QtGui import QFont, QFontMetricsF, QPainter
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene, QStyleOptionGraphicsItem, QWidget
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction

class BlockchainGraphics(QGraphicsItem):
    FontSize = 10
    Font = QFont("Courrier", FontSize)
    FontMetric = QFontMetricsF(Font)
    VertIncr = 0 # Espace en hauteur entre les différentes chaînes
    HorIncr = 15 # Espace sur les bords des blocs (et autre) pour respirer
    SpaceBetweenBlocks = 45 # Espace entre deux blocs

    def deleteGraphs(self, blockGraphs):
        for g in blockGraphs:
            self.scene.removeItem(g)

    def graphsFromChain(self, blocks, blockGraphs, h, color = Qt.black):  # Methode général de dessin, à partir d'une liste de graphs et de blocs, et de la hauteur. Ne gere par width et height
        # On rajoute les nouveaux
        blockGraphs.clear()
        for i in range(len(blocks)):
            b = blocks[i]
            graph = BlockGraphics(b,self, color)
            blockGraphs += [graph]
            graph.moveBy(i * (graph.width + BlockchainGraphics.SpaceBetweenBlocks), h)
    
    @Slot()
    def graphsFromValid(self):
        self.deleteGraphs(self.validBlockGraphs)
        self.graphsFromChain(self.blockchain.validBlocks, self.validBlockGraphs, 0)
        
        self.updateWidthHeight()


    @Slot()
    def graphsFromAlternate(self):
        if len(self.blockchain.alternateFollowingChains) > len(self.alternateBlockGraphss): # De nouvelle chaînes, on doit donc ajuster la taille
            self.alternateBlockGraphss += [[] for k in range(len(self.alternateBlockGraphss), len(self.blockchain.alternateFollowingChains))]
        for i in range(len(self.blockchain.alternateFollowingChains)): # Pour chaque chaines
            self.deleteGraphs(self.alternateBlockGraphss[i])
            self.graphsFromChain(self.blockchain.alternateFollowingChains[i], self.alternateBlockGraphss[i], (i+1) * (self.validBlockGraphs[-1].height + BlockchainGraphics.VertIncr), Qt.red) # Le dernier bloc donne une taille typique de bloc (pas 0 puisque bloc origine)
        
        self.updateWidthHeight()



    def updateWidthHeight(self):
        if len(self.alternateBlockGraphss) == 0: # Tout début vraiment rien
            self.width = 0
            self.height = 0
        elif len(self.alternateBlockGraphss[0]) == 0:
            self.width = len(max(self.blockchain.alternateFollowingChains, key=len)) * (self.validBlockGraphs[-1].width + BlockchainGraphics.SpaceBetweenBlocks) # Longueur de la plus longue
            self.height = self.validBlockGraphs[-1].height * (len(self.blockchain.alternateFollowingChains) + 1)
        else:
            self.width = len(max(self.blockchain.alternateFollowingChains, key=len)) * (self.alternateBlockGraphss[0][-1].width + BlockchainGraphics.SpaceBetweenBlocks) # Longueur de la plus longue
            self.height = (self.alternateBlockGraphss[0][-1].height + BlockchainGraphics.VertIncr) * (len(self.blockchain.alternateFollowingChains) + 1)



    def __init__(self, blockchain: Blockchain, scene : QGraphicsScene, parent: QGraphicsItem = None):
        super().__init__(parent)
        
        BlockchainGraphics.VertIncr = 1 * BlockchainGraphics.FontMetric.height()

        self.scene = scene

        self.blockchain = blockchain
        self.validBlockGraphs = []
        self.alternateBlockGraphss = [] # Chaque ligne sera une alternate a part, la colonne le bloc etc...
        self.graphsFromValid()
        self.graphsFromAlternate()

        self.updateWidthHeight()

        self.left = -5
        self.top = -BlockchainGraphics.VertIncr

        self.blockchain.updateSignal.connect(self.graphsFromValid)
        self.blockchain.updateSignal.connect(self.graphsFromAlternate)
    
    def boundingRect(self):
        return QRectF(self.left, self.top, self.width, self.height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        pass

class BlockGraphics(QGraphicsItem):

    def __init__(self, block: Block, parent: QGraphicsItem = None, color = Qt.black):
        super().__init__(parent)

        self.block = block
        self.color = color

        self.transactions = self.block.transactions
        self.transactionGraphs = []
        for i in range(len(self.transactions)):
            graph = TransactionGraphics(self.transactions[i], self)
            self.transactionGraphs += [graph]
            graph.moveBy(BlockchainGraphics.HorIncr, 5 * 1 * BlockchainGraphics.FontMetric.height() + i*graph.height + BlockchainGraphics.VertIncr) # Meme decalage que le debut de height

        if len(self.transactions) == 0 : # a priori c'est necessairement le bloc origine
            self.height = 5 * BlockchainGraphics.VertIncr
        else:
            self.height = (5+1) * BlockchainGraphics.VertIncr + len(self.transactions) * self.transactionGraphs[0].height
        self.width = BlockchainGraphics.FontMetric.horizontalAdvance("Last block hash : " + 'a'*64) + BlockchainGraphics.HorIncr
        self.left = -5
        self.top = -BlockchainGraphics.VertIncr


    def boundingRect(self):
        return QRectF(self.left, self.top, self.width, self.height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        vertIncr = BlockchainGraphics.VertIncr

        painter.setPen(self.color)

        painter.drawRect(QRectF(self.left, self.top, self.width, self.height))
        
        painter.setFont(BlockchainGraphics.Font)

        size = BlockchainGraphics.FontSize


        painter.drawText(0, 0, "id : " + str(self.block.blockId))

        painter.setFont(QFont("Courrier",size))
        painter.drawText(0, 1 * vertIncr, "Hash : " + hex(int(str(self.block.hashBlock()), 2)))
        painter.drawText(0, 2 * vertIncr, "Last block hash : " + hex(int(str(self.block.lbHash),2)))
        painter.drawText(0, 3 * vertIncr, "Proof of work : " + str(self.block.proofOfWork))
        painter.drawText(0, 4 * vertIncr, "Transactions : ")
            

class TransactionGraphics(QGraphicsItem):

    def __init__(self, transaction: Transaction, parent: QGraphicsItem = None):
        super().__init__(parent)
        self.transaction = transaction

        self.color = parent.color

        self.width = BlockchainGraphics.FontMetric.horizontalAdvance("Id de la personne : 000")
        self.height = 3.5 * BlockchainGraphics.VertIncr
        self.left = -5
        self.top = -BlockchainGraphics.VertIncr
        
    
    def boundingRect(self):
        return QRectF(self.left, self.top, self.width, self.height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        vertIncr = BlockchainGraphics.VertIncr

        painter.setPen(self.color)

        painter.drawRect(QRectF(self.left, self.top, self.width, self.height))

        painter.setFont(BlockchainGraphics.Font)

        painter.drawText(0, 0 * vertIncr, "Id de la personne : " + str(self.transaction.personId))
        painter.drawText(0, 1 * vertIncr, "Date : " + self.transaction.newDate)
        painter.drawText(0, 2 * vertIncr, "Id de la maladie : " + str(self.transaction.maladieId))

        