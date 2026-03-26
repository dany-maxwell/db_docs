from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QLineEdit, 
                               QDateEdit, QPushButton, QTextEdit, QMessageBox, QListWidget, QListWidgetItem)
from PySide6.QtCore import QDate, Qt

from ui.widgets.widgets import (
    MemoComboBox)

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_documentos_tramite)

from services.busqueda_service import (
    busqueda_por_memo)

from services.auditoria_service import (
    aplicar_impugnacion)
class WidgetImpugnacion(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        box_impugnacion = QGroupBox("Impugnacion")
        lay_impugnacion = QVBoxLayout()

        self.label_impugnacion = QLabel("Codigo:")
        self.line_impugnacion = QLineEdit()
        self.label_impugnacion_fecha = QLabel("Fecha:")
        self.date_impugnacion = QDateEdit()
        self.date_impugnacion.setCalendarPopup(True)
        self.date_impugnacion.setDate(QDate.currentDate())

        lay_impugnacion.addWidget(self.label_impugnacion)
        lay_impugnacion.addWidget(self.line_impugnacion)
        lay_impugnacion.addWidget(self.label_impugnacion_fecha)
        lay_impugnacion.addWidget(self.date_impugnacion)

        box_impugnacion.setLayout(lay_impugnacion)
        layout.addWidget(box_impugnacion)

        box_memo = QGroupBox("Memorando de Petición de PAS")
        lay_memo = QVBoxLayout()
        self.combo_memos = MemoComboBox([(None, "")] + catalogo_documentos(1))
        lay_memo.addWidget(self.combo_memos)
        self.label_proveedor = QLabel("Proveedor: ")
        lay_memo.addWidget(self.label_proveedor)
        self.label_cedula = QLabel("Cedula/Ruc: ")
        lay_memo.addWidget(self.label_cedula)

        box_memo.setLayout(lay_memo)
        layout.addWidget(box_memo)

        box_documentos = QGroupBox("Documentos Relacionados")
        lay_documentos = QVBoxLayout()

        self.list_documentos = QListWidget()

        lay_documentos.addWidget(self.list_documentos)
        box_documentos.setLayout(lay_documentos)
        layout.addWidget(box_documentos)

        self.btn_guardar = QPushButton("Guardar Impugnación")
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
        self.combo_memos.currentIndexChanged.connect(self.cargar_documentos)
        self.list_documentos.itemSelectionChanged.connect(self.mostrar_id)
        self.btn_guardar.clicked.connect(self.confirmar_impugnacion)

    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.label_proveedor.setText("Proveedor: ")
            self.label_cedula.setText("Cedula/Ruc: ")
            return
        info_memo = busqueda_por_memo(id_memo)
        self.label_proveedor.setText(f"Proveedor: {info_memo['proveedor']}")
        self.label_cedula.setText(f"Cedula/Ruc: {info_memo['cedula_ruc']}")
    def actualizar_combos(self):
            self.combo_memos._setup_items([(None, "")] + catalogo_documentos(1))
            self.list_documentos.clear()
            
    def cargar_documentos(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.list_documentos.clear()
            return
        documentos = catalogo_documentos_tramite(busqueda_por_memo(id_memo)['tramite'])
        self.list_documentos.clear()
        for d in documentos:
            item = QListWidgetItem(f"{d['codigo_final']} - {d['tipo']} {' - ' + d['subtipo'] if d['subtipo'] is not None else ''} - {d['fecha_documento']}")
            item.setData(Qt.UserRole, d['documento_id'])
            self.list_documentos.addItem(item)

    def mostrar_id(self):
        item = self.list_documentos.currentItem()
        if item:
            id_doc = item.data(Qt.UserRole)

    def confirmar_impugnacion(self):  
        id_memo = self.combo_memos.currentData()
        codigo = self.line_impugnacion.text()
        nombre_doc = self.list_documentos.currentItem().text() if self.list_documentos.currentItem() else None
        id_documento = self.list_documentos.currentItem().data(Qt.UserRole) if self.list_documentos.currentItem() else None

        if not codigo:
            QMessageBox.warning(self, "Error", "El código de impugnación es obligatorio.")
            return
        
        if not id_documento or not id_memo:
            QMessageBox.warning(self, "Error", "Debe seleccionar un documento relacionado.")
            return
        
        respuesta = QMessageBox.question(self, 
                    '¿Está seguro de continuar?',
                    f"Se archivarán todos los documentos desde el documento: \n{nombre_doc} \nen adelante",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.aplicar_impugnacion()

    def aplicar_impugnacion(self):
        id_memo = self.combo_memos.currentData()
        id_tramite = busqueda_por_memo(id_memo)[5] if id_memo else None
        codigo = self.line_impugnacion.text()
        fecha = self.date_impugnacion.date().toString("yyyy-MM-dd")
        id_documento = self.list_documentos.currentItem().data(Qt.UserRole) if self.list_documentos.currentItem() else None
        
        aplicar_impugnacion(
            codigo_impugnacion=codigo,
            fecha_impugnacion=fecha,
            tramite_id=id_tramite,
            documento_id=id_documento
        )
        QMessageBox.information(self, "Éxito", "Impugnación aplicada correctamente.")