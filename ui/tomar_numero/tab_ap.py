from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout

from .base_tab import BaseTabDocumento
from ui.widgets import OrigenComboBox
from services.catalogo_service import catalogo_documentos
from constants import TIPO_DOCUMENTO_AP, TIPO_DOCUMENTO_MEMO


class TabActuacionPrevia(BaseTabDocumento):

    def __init__(self):
        super().__init__()
        # Botón
        self.button_tomar_numero = QPushButton("Tomar Numero AP")
        self.layout.addWidget(self.button_tomar_numero)        # Conectar eventos
        self.button_tomar_numero.clicked.connect(self.tomar_numero)
    
    def actualizar_combos_extra(self):
            # No combos secundarios a refrescar
            pass
    
    def tomar_numero(self):
        self.crear_documento(TIPO_DOCUMENTO_AP)
