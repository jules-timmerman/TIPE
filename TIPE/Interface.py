from PySide6.QtWidgets import *


class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self._mainLayout = QHBoxLayout()

        self._mainMenuWidget = QWidget()
        self._mainMenuWidgetLayout = QGridLayout()

        self._etatWidget = QWidget()
        self._etatWidgetLayout = QGridLayout()

        ## Mise en place du Main Widget
        self._buttonTransaction = QPushButton("Generer une transaction")
        self._buttonMineur = QPushButton("Generer un mineur")
        self._buttonClient = QPushButton("Generer un client")
        self._buttonEtat = QPushButton("Etat du systeme")
        self._buttonSimulation = QPushButton("Simulation")
        self._buttonPause = QPushButton("Pause")

        self._buttonTransaction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonMineur.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonClient.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonEtat.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonSimulation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._buttonPause.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self._buttonTransaction.clicked.connect(self.genTransaction)
        self._buttonMineur.clicked.connect(self.genMineur)
        self._buttonClient.clicked.connect(self.genClient)
        self._buttonEtat.clicked.connect(self.etat)
        self._buttonSimulation.clicked.connect(self.simulation)
        self._buttonPause.clicked.connect(self.pause)

        self._mainMenuWidgetLayout.addWidget(self._buttonTransaction, 0, 0)
        self._mainMenuWidgetLayout.addWidget(self._buttonMineur, 0, 1)
        self._mainMenuWidgetLayout.addWidget(self._buttonClient, 1, 0)
        self._mainMenuWidgetLayout.addWidget(self._buttonEtat, 1, 1)
        self._mainMenuWidgetLayout.addWidget(self._buttonSimulation, 2, 0)
        self._mainMenuWidgetLayout.addWidget(self._buttonPause, 2, 1)

        ## **********************************
        ## Mise en place du (test) etatWidget

        self._listViewClient = QListView()
        self._listViewMineur = QListView()
        self._buttonRetour = QPushButton("Retour")

        self._buttonRetour.clicked.connect(self.retour)


        self._etatWidgetLayout.addWidget(self._listViewClient, 0, 0)
        self._etatWidgetLayout.addWidget(self._listViewMineur, 0, 1)
        self._etatWidgetLayout.addWidget(self._buttonRetour, 1, 0, 1, 2)

        ## **********************************

        self._mainLayout.addWidget(self._mainMenuWidget)


        ## On set tout les Layouts
        self._mainMenuWidget.setLayout(self._mainMenuWidgetLayout)
        self._etatWidget.setLayout(self._etatWidgetLayout)
        self.setLayout(self._mainLayout)

        self.setWindowTitle("Blockchain TIPE")


    def genTransaction(self):
        pass

    def genMineur(self):
        pass

    def genClient(self):
        pass

    def etat(self):
        self._mainLayout.replaceWidget(self._mainMenuWidget, self._etatWidget)
        self._etatWidget.show()
        self._mainMenuWidget.hide()

    def simulation(self):
        pass

    def pause(self):
        pass
    def retour(self):
        self._mainLayout.replaceWidget(self._etatWidget, self._mainMenuWidget)
        self._mainMenuWidget.show()
        self._etatWidget.hide()












