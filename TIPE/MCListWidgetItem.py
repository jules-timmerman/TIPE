from PySide6.QtWidgets import QListWidgetItem

class MCListWidgetItem(QListWidgetItem):
    
    def __init__(self, mc, text, listview): # MC est un mineur ou client au choix
        super().__init__(text, listview)
        self.mc = mc
