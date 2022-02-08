from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget
from Block import Block
from Blockchain import Blockchain

class BlockchainGraphics(QGraphicsItem):
    def BlockchainGraphics(blockchain: Blockchain):
        pass
    
    def boundingRect(self):
        pass

    def paint(self, painter, option = QStyleOptionGraphicsItem(), widget = QWidget()):
        pass

class BlockGraphics(QGraphicsItem):

    def BlockGraphics(self, block: Block):
        self.block = block

        self.width = 80
        self.height = 10
        self.left = 0
        self.top = 0


    def boundingRect(self):
        return QRectF(self.left, self.top, self.width, self.height)

    def paint(self, painter, option = QStyleOptionGraphicsItem(), widget = QWidget()):
        pass