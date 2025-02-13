from PyQt5.QtWidgets import QWidget

class BaseScreen(QWidget):
    def __init__(self):
        super().__init__()
        # Shared properties or methods can go here
        self.setStyleSheet("font-size: 14px;")  # Example shared styling
