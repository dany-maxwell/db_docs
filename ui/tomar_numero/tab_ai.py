from PySide6.QtWidgets import ( QWidget, QVBoxLayout, QLabel,
QComboBox )

from ui.widgets import MemosComboBox

from services.catalogo_service import catalogo_memorando_inicio_pas

class TabActoInicio(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Memorando de Peticion de PAS"))
        self.combo_memos = QComboBox()
        items = catalogo_memorando_inicio_pas()
        layout.addWidget(MemosComboBox(items))



        self.setLayout(layout)

        
