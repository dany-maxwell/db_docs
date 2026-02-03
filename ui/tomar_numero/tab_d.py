from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TabDictamen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("DICTAMEN - Pendiente"))

        self.setLayout(layout)
