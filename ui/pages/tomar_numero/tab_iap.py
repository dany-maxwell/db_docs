from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout, QComboBox, QMessageBox

from .base_tab import BaseTabDocumento
from ui.widgets.widgets import OrigenComboBox, TipoComboBox
from services.catalogo_service import catalogo_documentos, catalogo_subtipos
from services.busqueda_service import busqueda_por_memo
from services.auditoria_service import prosigue_tramite
from constants import TIPO_DOCUMENTO_IAP, TIPO_DOCUMENTO_AP, SUBTIPO_IAP
class TabInformeAP(BaseTabDocumento):
    def __init__(self):
        super().__init__()
        self.ui()
    
    def ui(self):
        box_origen = QGroupBox("Actuacion Previa Correspondiente")
        lay_origen = QVBoxLayout()
        self.combo_origen = OrigenComboBox(catalogo_documentos(TIPO_DOCUMENTO_AP))
        lay_origen.addWidget(self.combo_origen)
        box_origen.setLayout(lay_origen)
        self.layout.addWidget(box_origen)
        
        box_tipo = QGroupBox("Tipo de Informe de Actuación Previa")
        lay_tipo = QVBoxLayout()
        self.combo_iap = TipoComboBox(catalogo_subtipos(SUBTIPO_IAP), with_completer=False)
        self.combo_iap.setEditable(False)
        lay_tipo.addWidget(self.combo_iap)
        box_tipo.setLayout(lay_tipo)
        self.layout.addWidget(box_tipo)
        
        self.box_prosigue = QGroupBox("Prosigue a PAS?")
        self.lay_prosigue = QVBoxLayout()
        self.combo_prosigue = QComboBox()
        self.combo_prosigue.addItem("Sí", True)
        self.combo_prosigue.addItem("No", False)
        self.lay_prosigue.addWidget(self.combo_prosigue)
        self.box_prosigue.setLayout(self.lay_prosigue)
        self.layout.addWidget(self.box_prosigue)
        self.box_prosigue.hide()

        self.button_tomar_numero = QPushButton("Tomar Numero IAP")
        self.layout.addWidget(self.button_tomar_numero)
        
        self.combo_memos.currentIndexChanged.connect(
            lambda: self.filtrar_origen(TIPO_DOCUMENTO_AP)
        )
        self.combo_iap.currentIndexChanged.connect(self.cuadro_prosigue)
        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)
    
    def cuadro_prosigue(self):
        if self.combo_iap.currentData() == 2:
            self.box_prosigue.show()
        else:
            self.box_prosigue.hide()

    def filtrar_origen_custom(self):
        self.filtrar_origen(TIPO_DOCUMENTO_AP)

    def actualizar_combos_extra(self):
        self.combo_iap._setup_items(catalogo_subtipos(SUBTIPO_IAP))
    
    def tomar_numero(self):
        try:
            id_tramite = busqueda_por_memo(id_memo=self.combo_memos.currentData())
            id_origen = self.combo_origen.currentData()
            id_subtipo = self.combo_iap.currentData()
            self.crear_documento(TIPO_DOCUMENTO_IAP, subtipo_documento_id=id_subtipo, 
                            documento_origen_id=id_origen)
            prosigue_tramite(self.combo_prosigue.currentData(), id_tramite['tramite'])
            self.box_prosigue.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", f"No se pudo completar la operación:\n{e}")
