from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout

from .base_tab import BaseTabDocumento
from ui.widgets import OrigenComboBox, TipoComboBox
from services.catalogo_service import catalogo_documentos, catalogo_subtipos
from constants import TIPO_DOCUMENTO_IJ, TIPO_DOCUMENTO_AI, SUBTIPO_IJ


class TabInformeJuridico(BaseTabDocumento):
    def __init__(self):
        super().__init__()
        
        # Tipo IJ
        box_ij = QGroupBox("Tipo de Informe Jurídico")
        lay_ij = QVBoxLayout()
        self.combo_ij = TipoComboBox(catalogo_subtipos(SUBTIPO_IJ))
        lay_ij.addWidget(self.combo_ij)
        box_ij.setLayout(lay_ij)
        self.layout.addWidget(box_ij)
        
        # Origen
        self.box_origen = QGroupBox("Acto de Inicio Correspondiente")
        lay_origen = QVBoxLayout()
        self.combo_origen = OrigenComboBox(catalogo_documentos(TIPO_DOCUMENTO_AI))
        lay_origen.addWidget(self.combo_origen)
        self.box_origen.setLayout(lay_origen)
        self.layout.addWidget(self.box_origen)
        self.box_origen.hide()
        
        # Botón
        self.button_tomar_numero = QPushButton("Tomar Numero IAP")
        self.layout.addWidget(self.button_tomar_numero)
        
        # Conectar eventos
        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
        self.combo_memos.currentIndexChanged.connect(
            lambda: self.filtrar_origen(TIPO_DOCUMENTO_AI)
        )
        self.combo_ij.currentIndexChanged.connect(self.mostrar_origen)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)
    
    def filtrar_origen_custom(self):
        self.filtrar_origen(TIPO_DOCUMENTO_AI)
    
    def mostrar_origen(self):
        idx_tipo = self.combo_ij.currentIndex()
        self.box_origen.setVisible(idx_tipo == 0)


    def actualizar_combos_extra(self):
        self.combo_ij._setup_items(catalogo_subtipos(SUBTIPO_IJ))
    
    def tomar_numero(self):
        id_origen = self.combo_origen.currentData()
        if not id_origen:
            return
        id_subtipo = self.combo_ij.currentData()
        self.crear_documento(TIPO_DOCUMENTO_IJ, subtipo_documento_id=id_subtipo,
                           documento_origen_id=id_origen)