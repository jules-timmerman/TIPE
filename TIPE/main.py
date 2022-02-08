import sys
from Interface import Interface
from testQtGraphics import testQtGraphics
from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Interface()
    widget.resize(800, 600)
    widget.show()

    #widget = testQtGraphics()
    #widget.resize(800,600)
    #widget.show()

    #widget.view.translate(100,100)


    sys.exit(app.exec())
    