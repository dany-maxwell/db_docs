from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout

from .base_tab import BaseTabDocumento
from ui.widgets import OrigenComboBox
from services.catalogo_service import catalogo_documentos
from constants import TIPO_DOCUMENTO_D, TIPO_DOCUMENTO_AI


class TabDictamen(BaseTabDocumento):
    def __init__(self):
        super().__init__()
        
        box_origen = QGroupBox("Acto de Inicio Correspondiente")
        lay_origen = QVBoxLayout()
        self.combo_origen = OrigenComboBox(catalogo_documentos(TIPO_DOCUMENTO_AI))
        lay_origen.addWidget(self.combo_origen)
        box_origen.setLayout(lay_origen)
        self.layout.addWidget(box_origen)
        
        self.button_tomar_numero = QPushButton("Tomar Numero IAP")
        self.layout.addWidget(self.button_tomar_numero)
        
        self.combo_memos.currentIndexChanged.connect(
            lambda: self.filtrar_origen(TIPO_DOCUMENTO_AI)
        )
        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)
    
    def filtrar_origen_custom(self):
        self.filtrar_origen(TIPO_DOCUMENTO_AI)


    def actualizar_combos_extra(self):
        pass
    
    def tomar_numero(self):
        id_origen = self.combo_origen.currentData()
        self.crear_documento(TIPO_DOCUMENTO_D, documento_origen_id=id_origen)
