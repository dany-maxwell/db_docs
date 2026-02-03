from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TabProvidencia(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("PROVIDENCIA - Pendiente"))

        self.setLayout(layout)
