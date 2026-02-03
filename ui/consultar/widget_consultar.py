from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class WidgetConsultar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Módulo CONSULTAS (pendiente)"))

        self.setLayout(layout)
