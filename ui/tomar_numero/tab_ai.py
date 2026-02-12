from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidget

from .base_tab import BaseTabDocumento
from ui.widgets import OrigenComboBox, InfraccionComboBox
from services.catalogo_service import catalogo_documentos, catalogo_infracciones
from services.numeracion_service import agregar_infraccion
from constants import TIPO_DOCUMENTO_IAP, MSG_YA_AGREGADO, TIPO_DOCUMENTO_AI


class TabActoInicio(BaseTabDocumento):
    def __init__(self):
        super().__init__()
        box_origen = QGroupBox("Informe FINAL de Actuación Previa")
        lay_origen = QVBoxLayout()
        self.combo_origen = OrigenComboBox(catalogo_documentos(TIPO_DOCUMENTO_IAP, 2))
        lay_origen.addWidget(self.combo_origen)
        box_origen.setLayout(lay_origen)
        self.layout.addWidget(box_origen)
        
        box_inf = QGroupBox("Infracciones")
        lay_inf = QVBoxLayout()
        self.combo_inf = InfraccionComboBox(catalogo_infracciones())
        lay_inf.addWidget(self.combo_inf)
        
        botones_inf = QHBoxLayout()
        self.btn_add_inf = QPushButton("Añadir")
        self.btn_del_inf = QPushButton("Quitar")
        botones_inf.addWidget(self.btn_add_inf)
        botones_inf.addWidget(self.btn_del_inf)
        lay_inf.addLayout(botones_inf)
        
        self.list_inf = QListWidget()
        lay_inf.addWidget(self.list_inf)
        box_inf.setLayout(lay_inf)
        self.layout.addWidget(box_inf)
        
        self.button_tomar_numero = QPushButton("Tomar Numero AI")
        self.layout.addWidget(self.button_tomar_numero)
        
        self.infracciones_seleccionadas = []
        
        self.combo_memos.currentIndexChanged.connect(
            lambda: self.filtrar_origen(TIPO_DOCUMENTO_IAP, 2)
        )
        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
        self.btn_add_inf.clicked.connect(self.agregar_infraccion)
        self.btn_del_inf.clicked.connect(self.quitar_infraccion)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)
    
    def filtrar_origen_custom(self):
        self.filtrar_origen(TIPO_DOCUMENTO_IAP, 2)
    
    def agregar_infraccion(self):
        id_infraccion = self.combo_inf.currentData()
        texto = self.combo_inf.currentText()
        
        if not id_infraccion or id_infraccion in self.infracciones_seleccionadas:
            if id_infraccion in self.infracciones_seleccionadas:
                QMessageBox.warning(self, "Aviso", MSG_YA_AGREGADO)
            return
        
        self.infracciones_seleccionadas.append(id_infraccion)
        self.list_inf.addItem(texto)
    
    def quitar_infraccion(self):
        fila = self.list_inf.currentRow()
        if fila >= 0:
            self.list_inf.takeItem(fila)
            del self.infracciones_seleccionadas[fila]
    

    def actualizar_combos_extra(self):
        self.combo_inf._setup_items(catalogo_infracciones())
        self.list_inf.clear()
        self.infracciones_seleccionadas.clear()
        
    def tomar_numero(self):
        id_origen = self.combo_origen.currentData()
        infracciones_a_guardar = list(self.infracciones_seleccionadas)
        resultado = self.crear_documento(TIPO_DOCUMENTO_AI, documento_origen_id=id_origen)
        if resultado:
            for inf in infracciones_a_guardar:
                agregar_infraccion(resultado["id"], inf)
            self.infracciones_seleccionadas.clear()
            self.list_inf.clear()
