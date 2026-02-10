from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class ActionButton(QWidget):
    def __init__(self, text, callback):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        self.btn = QPushButton(text)
        self.btn.setFixedWidth(80)
        self.btn.clicked.connect(callback)

        layout.addWidget(self.btn)
        layout.setAlignment(Qt.AlignCenter)