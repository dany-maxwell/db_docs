from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout

from .base_tab import BaseTabDocumento
from ui.widgets import OrigenComboBox
from services.catalogo_service import catalogo_documentos
from services.busqueda_service import busqueda_por_memo
from services.auditoria_service import actualizar_estado
from constants import TIPO_DOCUMENTO_AP, TIPO_DOCUMENTO_MEMO


class TabActuacionPrevia(BaseTabDocumento):

    def __init__(self):
        super().__init__()
        self.button_tomar_numero = QPushButton("Tomar Numero AP")
        self.layout.addWidget(self.button_tomar_numero)       
        self.button_tomar_numero.clicked.connect(self.tomar_numero)
    
    def actualizar_combos_extra(self):
            pass
    
    def tomar_numero(self):
        tramite_id = busqueda_por_memo(id_memo=self.combo_memos.currentData())
        self.crear_documento(TIPO_DOCUMENTO_AP)
        actualizar_estado(3, tramite_id[2])
