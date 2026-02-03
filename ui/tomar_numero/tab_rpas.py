from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TabResolucion(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("RESOLUCIÓN - Pendiente"))

        self.setLayout(layout)
