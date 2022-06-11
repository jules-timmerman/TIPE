import sys

from PySide6.QtWidgets import QApplication
from Interface import Interface

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Interface()
    widget.resize(800, 600)
    widget.show()


    sys.exit(app.exec())
    