from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class WidgetCrearTramite(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Módulo CREAR TRÁMITE (pendiente)"))

        self.setLayout(layout)
