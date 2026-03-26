from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout, QMessageBox

from .base_tab import BaseTabDocumento
from ui.widgets.widgets import OrigenComboBox
from services.catalogo_service import catalogo_documentos
from services.busqueda_service import busqueda_por_memo
from services.auditoria_service import actualizar_estado
from constants import TIPO_DOCUMENTO_AP


class TabActuacionPrevia(BaseTabDocumento):

    def __init__(self):
        super().__init__()
        self.button_tomar_numero = QPushButton("Tomar Numero AP")
        self.layout.addWidget(self.button_tomar_numero)       
        self.button_tomar_numero.clicked.connect(self.tomar_numero)
    
    def actualizar_combos_extra(self):
            pass
    
    def tomar_numero(self):
        try:
            id_memo = self.combo_memos.currentData()
            if not id_memo:
                QMessageBox.warning(self, "Advertencia", "Selecciona un memorando primero.") 
                return
            tramite_id = busqueda_por_memo(id_memo=self.combo_memos.currentData())
            if not tramite_id:
                QMessageBox.warning(self, "Error", "No se encontró el trámite asociado.")
                return
            self.crear_documento(TIPO_DOCUMENTO_AP, documento_origen_id=self.combo_memos.currentData())
            actualizar_estado(3, tramite_id['tramite'])
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", f"No se pudo completar la operación:\n{e}")