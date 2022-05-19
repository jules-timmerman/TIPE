from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QHBoxLayout, QWidget
from Block import Block
from Block import hash
from Blockchain import Blockchain
from BlockchainHUD import BlockGraphics, BlockchainGraphics, TransactionGraphics
from Transaction import Transaction


class testQtGraphics(QWidget):
    
    def __init__(self):
        super().__init__()

        self.scene= QGraphicsScene()

        #self.rect1 = self.scene.addRect(0,0,50,50)
        #self.rect1.setRotation(45)
        #self.rect1.setScale(2)

        trans = Transaction(1,2,"30/04/2002",3)

        #transGraph = TransactionGraphics(trans)
        #self.scene.addItem(transGraph)

        block = Block(1, hash('a',0), [trans, trans], 3)
        #blockGraph = BlockGraphics(block)
        #self.scene.addItem(blockGraph)

        #blockGraph2 = BlockGraphics(block)
        #blockGraph2.moveBy(blockGraph2.width, 0)
        #self.scene.addItem(blockGraph2)

        #blockGraph3 = BlockGraphics(block)
        #blockGraph3.moveBy(5 * blockGraph3.width, 0)
        #self.scene.addItem(blockGraph3)

        blockchain = Blockchain()
        #blockchain.validBlocks += [block, block, block]
        blockchainGraph = BlockchainGraphics(blockchain)
        self.scene.addItem(blockchainGraph)
        #print(blockchainGraph.validBlockGraphs[1].width)
        #blockchain.alternateFollowingChains += [[block]] # Oui c'est bien un pointeur donc on pourra modifier la chaine et juste appeler une modification graphique
        #blockchain.validBlocks += [block]
        self.view = QGraphicsView(self.scene)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        blockchain.chainUpdate()
