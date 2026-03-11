from PySide6.QtWidgets import QPushButton, QRadioButton, QHBoxLayout, QDateEdit, QComboBox, QGroupBox, QVBoxLayout
from PySide6.QtCore import QDate

from .base_tab import BaseTabDocumento
from ui.widgets.widgets import OrigenComboBox, TipoComboBox
from services.catalogo_service import catalogo_documentos, catalogo_subtipos
from constants import (TIPO_DOCUMENTO_AP, TIPO_DOCUMENTO_AI, TIPO_DOCUMENTO_PR,
                       SUBTIPO_PR_AP, SUBTIPO_PR_INSTR, SUBTIPO_PR_RES)


class TabProvidencia(BaseTabDocumento):
    def __init__(self):
        super().__init__()
        self.ui()
    
    def ui(self):
        self.radio_ap = QRadioButton("En Actuación Previa")
        self.radio_instr = QRadioButton("En Instrucción")
        self.radio_res = QRadioButton("En Resolución")
        self.radio_ap.setChecked(True)

        radios = QHBoxLayout()
        radios.addWidget(self.radio_ap)
        radios.addWidget(self.radio_instr)
        radios.addWidget(self.radio_res)
        self.layout.insertLayout(0, radios)

        self.box_origen = QGroupBox("")
        lay_origen = QVBoxLayout()
        self.combo_origen = OrigenComboBox([])
        lay_origen.addWidget(self.combo_origen)
        self.box_origen.setLayout(lay_origen)
        self.layout.addWidget(self.box_origen)

        self.box_tipo = QGroupBox("Tipo")
        lay_tipo = QVBoxLayout()
        self.combo_tipo = TipoComboBox(catalogo_subtipos(SUBTIPO_PR_INSTR))
        self.combo_tipo.setEditable(False)
        lay_tipo.addWidget(self.combo_tipo)
        self.box_tipo.setLayout(lay_tipo)
        self.layout.addWidget(self.box_tipo)
        self.box_tipo.hide()

        self.box_fecha = QGroupBox()
        layout_fecha = QHBoxLayout()

        box_mAplazados = QGroupBox("Meses que se aplaza")
        lay_mAplazados = QVBoxLayout()
        self.combo_mes = QComboBox()
        self.combo_mes.addItem("1", 1)
        self.combo_mes.addItem("2", 2)
        lay_mAplazados.addWidget(self.combo_mes)
        box_mAplazados.setLayout(lay_mAplazados)

        box_fechaI = QGroupBox("Fecha desde la cual se aplaza")
        lay_fechaI = QVBoxLayout()
        self.edit_fecha = QDateEdit()
        self.edit_fecha.setDate(QDate.currentDate())
        self.edit_fecha.setCalendarPopup(True)
        lay_fechaI.addWidget(self.edit_fecha)
        box_fechaI.setLayout(lay_fechaI)

        layout_fecha.addWidget(box_mAplazados)
        layout_fecha.addWidget(box_fechaI)
        self.box_fecha.setLayout(layout_fecha)
        self.layout.addWidget(self.box_fecha)
        self.box_fecha.hide()

        self.button_tomar_numero = QPushButton("Tomar Numero Providencias")
        self.layout.addWidget(self.button_tomar_numero)

        self.radio_ap.toggled.connect(self.cambiar_modo)
        self.radio_instr.toggled.connect(self.cambiar_modo)
        self.radio_res.toggled.connect(self.cambiar_modo)

        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
        self.combo_memos.currentIndexChanged.connect(lambda: self.filtrar_origen_custom())
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

        self.cambiar_modo()

    def cambiar_modo(self):
        self.combo_memos.setCurrentIndex(0)
        
        if self.radio_ap.isChecked():
            self.box_origen.setTitle("Actuacion Previa")
            items = catalogo_documentos(TIPO_DOCUMENTO_AP)
            self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
            self.combo_origen.actualizar_items(items)
            self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
            self.box_tipo.hide()
            self.box_fecha.hide()
        
        elif self.radio_instr.isChecked():
            self.box_origen.setTitle("Acto de Inicio")
            items = catalogo_documentos(TIPO_DOCUMENTO_AI)
            self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
            self.combo_origen.actualizar_items(items)
            self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
            self.box_tipo.show()
            self.box_fecha.hide()
        
        elif self.radio_res.isChecked():
            self.box_origen.setTitle("Acto de Inicio")
            items = catalogo_documentos(TIPO_DOCUMENTO_AI)
            self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
            self.combo_origen.actualizar_items(items)
            self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
            self.box_tipo.hide()
            self.box_fecha.show()

    def filtrar_origen_custom(self):
        tipo_id = TIPO_DOCUMENTO_AP if self.radio_ap.isChecked() else TIPO_DOCUMENTO_AI
        self.filtrar_origen(tipo_id)
    

    def actualizar_combos_extra(self):
        self.combo_tipo.clear()
        self.combo_mes.setCurrentIndex(0)
        self.edit_fecha.setDate(QDate.currentDate())

    def tomar_numero(self):
        id_origen = self.combo_origen.currentData()
        if not id_origen:
            return
        
        if self.radio_ap.isChecked():
            id_subtipo = SUBTIPO_PR_AP
        elif self.radio_instr.isChecked():
            id_subtipo = self.combo_tipo.currentData()
        else: 
            id_subtipo = SUBTIPO_PR_RES
        
        self.crear_documento(TIPO_DOCUMENTO_PR, subtipo_documento_id=id_subtipo,
                           documento_origen_id=id_origen)
