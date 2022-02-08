from PySide6.QtWidgets import *


class testQtGraphics(QWidget):
    def __init__(self):
        super().__init__()

        self.scene= QGraphicsScene()

        self.rect1 = self.scene.addRect(0,0,50,50)
        self.rect1.setRotation(45)
        self.rect1.setScale(2)


        self.view = QGraphicsView(self.scene)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        
        self.view.rotate(45)



