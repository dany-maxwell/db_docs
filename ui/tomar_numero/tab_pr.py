from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QRadioButton, QHBoxLayout, QDateEdit, QComboBox, QGroupBox)
from PySide6.QtCore import QDate
from ui.widgets import (
    MemoComboBox,
    OrigenComboBox,
    TipoComboBox)

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_subtipos)

from services.busqueda_service import (
    busqueda_por_memo,
    busqueda_id_memo_por_documento)

from services.numeracion_service import (
    crear_documento_con_numeracion)
class TabProvidencia(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.radio_ap = QRadioButton("En Actuación Previa")
        self.radio_instr = QRadioButton("En Instrucción")
        self.radio_res = QRadioButton("En Resolución")

        self.radio_ap.setChecked(True)

        radios = QHBoxLayout()
        radios.addWidget(self.radio_ap)
        radios.addWidget(self.radio_instr)
        radios.addWidget(self.radio_res)

        layout.addLayout(radios)

        box_memo = QGroupBox("Memorando de Petición de PAS")
        lay_memo = QVBoxLayout()

        self.combo_memos = MemoComboBox([(None, "- Sin Seleccionar -")] + catalogo_documentos(1))
        lay_memo.addWidget(self.combo_memos)

        lay_memo.addWidget(QLabel("Proveedor:"))
        self.label_proveedor = QLabel("")
        lay_memo.addWidget(self.label_proveedor)

        box_memo.setLayout(lay_memo)
        layout.addWidget(box_memo)

        self.box_origen = QGroupBox("")
        lay_origen = QVBoxLayout()

        items = []
        self.combo_origen = OrigenComboBox(items)
        lay_origen.addWidget(self.combo_origen)

        self.box_origen.setLayout(lay_origen)
        layout.addWidget(self.box_origen)

        self.box_tipo = QGroupBox("Tipo")
        lay_tipo = QVBoxLayout()

        self.combo_tipo = TipoComboBox(items)
        lay_tipo.addWidget(self.combo_tipo)

        self.box_tipo.setLayout(lay_tipo)
        layout.addWidget(self.box_tipo)

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
        layout.addWidget(self.box_fecha)

        self.button_tomar_numero = QPushButton("Tomar Numero IAP")
        layout.addWidget(self.button_tomar_numero)

        self.setLayout(layout)

        self.radio_ap.toggled.connect(self.cambiar_modo)
        self.radio_instr.toggled.connect(self.cambiar_modo)
        self.radio_res.toggled.connect(self.cambiar_modo)

        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_origen)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

        self.cambiar_modo()

    def cambiar_modo(self):
        if self.radio_ap.isChecked():
            self.combo_memos.setCurrentIndex(0)

            self.box_origen.setTitle("Actuacion Previa")

            ap_items = catalogo_documentos(4)
            self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
            self.combo_origen.actualizar_items(ap_items)
            self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)

            self.box_tipo.hide()

            self.box_fecha.hide()

        elif self.radio_instr.isChecked():
            self.combo_memos.setCurrentIndex(0)

            self.box_origen.setTitle("Acto de Inicio")

            ai_items = catalogo_documentos(6)
            self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
            self.combo_origen.actualizar_items(ai_items)
            self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
            
            tipo_items = catalogo_subtipos(7)
            self.combo_tipo.actualizar_items(tipo_items)
            
            self.box_tipo.show()
            self.box_fecha.hide()


        elif self.radio_res.isChecked():
            self.combo_memos.setCurrentIndex(0)

            self.box_origen.setTitle("Acto de Inicio")

            ai_items = catalogo_documentos(6)
            self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
            self.combo_origen.actualizar_items(ai_items)
            self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)

            self.box_tipo.hide()
            self.box_fecha.show()

    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.label_proveedor.setText("")
            return
        proveedor = busqueda_por_memo(id_memo)[0]
        

        self.label_proveedor.setText(proveedor)

    def filtrar_origen (self):
        id_memo = self.combo_memos.currentData()
        if self.radio_ap.isChecked():
            tipo_id = 4
        else:
            tipo_id = 6

        if not id_memo:
            new_items = catalogo_documentos(6)
        else:
            tramite = busqueda_por_memo(id_memo)[2]
            new_items = catalogo_documentos(tipo_id, None, tramite)
        
        self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
        self.combo_origen.actualizar_items(new_items)
        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)

    def filtrar_mem (self):
        id_tramite = self.combo_origen.currentData()
        id_memo = busqueda_id_memo_por_documento(id_tramite)
        self.combo_memos.currentIndexChanged.disconnect(self.filtrar_origen)
        self.combo_memos.actualizar_index(id_memo)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_origen)

    def tomar_numero(self):
        id_memo = self.combo_memos.currentData()
        id_origen = self.combo_origen.currentData()
        id_subtipo = 0

        if self.radio_ap.isChecked():
            id_subtipo = 3
        elif self.radio_instr.isChecked():
            id_subtipo = self.combo_tipo.currentData()
        elif self.radio_res.isChecked():
            id_subtipo = 9
    
        resultado = crear_documento_con_numeracion(
            tramite_id=busqueda_por_memo(id_memo)[2],
            tipo_documento_id=7,
            subtipo_documento_id=id_subtipo,
            documento_origen_id=id_origen,
            codigo_manual=None,
            unidad_codigo=busqueda_por_memo(id_memo)[1]
        )

        QMessageBox.information(
            self,
            "Número tomado",
            f"Código: {resultado['codigo']}\n"
            f"Fecha: {resultado['fecha']}"
        )
