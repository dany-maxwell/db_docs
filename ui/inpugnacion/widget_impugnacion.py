from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QLineEdit, 
                               QDateEdit, QPushButton, QTextEdit, QMessageBox, QListWidget)
from PySide6.QtCore import QDate

from ui.widgets import (
    MemoComboBox)

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_documentos_tramite)

from services.busqueda_service import (
    busqueda_por_memo)

class WidgetImpugnacion(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        box_inpugnacion = QGroupBox("Impugnacion")
        lay_inpugnacion = QVBoxLayout()

        self.label_impugnacion = QLabel("Codigo:")
        self.line_impugnacion = QLineEdit()
        self.label_impugnacion_fecha = QLabel("Fecha:")
        self.date_impugnacion = QDateEdit()
        self.date_impugnacion.setCalendarPopup(True)
        self.date_impugnacion.setDate(QDate.currentDate())

        lay_inpugnacion.addWidget(self.label_impugnacion)
        lay_inpugnacion.addWidget(self.line_impugnacion)
        lay_inpugnacion.addWidget(self.label_impugnacion_fecha)
        lay_inpugnacion.addWidget(self.date_impugnacion)

        box_inpugnacion.setLayout(lay_inpugnacion)
        layout.addWidget(box_inpugnacion)

        box_memo = QGroupBox("Memorando de Petición de PAS")
        lay_memo = QVBoxLayout()
        self.combo_memos = MemoComboBox([(None, "- Sin Seleccionar -")] + catalogo_documentos(1))
        lay_memo.addWidget(self.combo_memos)
        lay_memo.addWidget(QLabel("Proveedor:"))
        self.label_proveedor = QLabel("")
        lay_memo.addWidget(self.label_proveedor)

        box_memo.setLayout(lay_memo)
        layout.addWidget(box_memo)

        box_documentos = QGroupBox("Documentos Relacionados")
        lay_documentos = QVBoxLayout()

        self.list_documentos = QListWidget()

        lay_documentos.addWidget(self.list_documentos)
        box_documentos.setLayout(lay_documentos)
        layout.addWidget(box_documentos)

        self.setLayout(layout)

        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
        self.combo_memos.currentIndexChanged.connect(self.cargar_documentos)

    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.label_proveedor.setText("")
            return
        proveedor = busqueda_por_memo(id_memo)[0]
        self.label_proveedor.setText(proveedor)
    def actualizar_combos(self):
            # Refresca el combo de memos y documentos relacionados
            self.combo_memos._setup_items([(None, "- Sin Seleccionar -")] + catalogo_documentos(1))
            self.list_documentos.clear()
            
    def cargar_documentos(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.list_documentos.clear()
            return
        documentos = catalogo_documentos_tramite(busqueda_por_memo(id_memo)[2])
        for d in documentos:
            self.list_documentos.addItem(f"{d[0]} - {d[1]} - {d[2]} - {d[3]}")