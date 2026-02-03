from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TabInformeJuridico(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("INFORME JURÍDICO - Pendiente"))

        self.setLayout(layout)
