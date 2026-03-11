from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QDateEdit, QMessageBox
from PySide6.QtCore import QDate
from ui.widgets.widgets import TipoComboBox, OrigenComboBox
from .base_tab import BaseTabDocumento

from services.busqueda_service import busqueda_por_memo, busqueda_info_documento
from services.catalogo_service import catalogo_tipos_extra, catalogo_subtipos, catalogo_documentos, catalogo_tipos
from services.auditoria_service import anadir_documento_manual

class TabDocumentoExtra(BaseTabDocumento):
    def __init__(self):
        super().__init__()
        self.ui()

    def ui (self):
        box_origen = QGroupBox('Documento "Origen": ')
        lay_origen = QHBoxLayout()
        self.combo_origen = OrigenComboBox([])
        lay_origen.addWidget(self.combo_origen)
        self.label_origen = QLabel("Tipo Documento Origen: --")
        lay_origen.addWidget(self.label_origen)
        box_origen.setLayout(lay_origen)
        self.layout.addWidget(box_origen)

        box_documento = QGroupBox("Documento: ")
        lay_documento = QVBoxLayout()

        self.combo_tipos = TipoComboBox(catalogo_tipos_extra())
        lay_documento.addWidget(self.combo_tipos)
        lay_documento.addWidget(QLabel('Tipo: '))
        self.combo_subtipos = TipoComboBox(catalogo_documentos())
        lay_documento.addWidget(self.combo_subtipos)

        lay_datos = QHBoxLayout()
        lay_codigo = QVBoxLayout()
        lay_codigo.addWidget(QLabel('Codigo: '))
        self.line_codigo = QLineEdit()
        lay_codigo.addWidget(self.line_codigo)
        lay_datos.addLayout(lay_codigo)

        lay_fecha = QVBoxLayout()
        lay_fecha.addWidget(QLabel('Fecha: '))
        self.date_fecha = QDateEdit(QDate.currentDate())
        self.date_fecha.setCalendarPopup(True)
        lay_fecha.addWidget(self.date_fecha)
        lay_datos.addLayout(lay_fecha)

        lay_documento.addLayout(lay_datos)
        box_documento.setLayout(lay_documento)

        self.layout.addWidget(box_documento)

        self.btn_anadir = QPushButton('Añadir/Adjuntar Documento "Extra"')
        self.layout.addWidget(self.btn_anadir)

        self.combo_memos.currentIndexChanged.connect(self.filtrar_origen_custom)
        self.combo_origen.currentIndexChanged.connect(self.mostrar_tipo_origen)
        self.combo_tipos.currentIndexChanged.connect(self.filtrar_subtipos)
        self.btn_anadir.clicked.connect(self.adjuntar_documento)

    def actualizar_combos_extra(self):
        self.combo_origen.setCurrentIndex(-1)
        self.combo_tipos.setCurrentIndex(-1)
        self.combo_subtipos.setCurrentIndex(-1)
        self.line_codigo.clear()
        self.date_fecha.setDate(QDate.currentDate())

    def filtrar_origen_custom(self):
        memo = self.combo_memos.currentData()
        if memo is None:
            return
        tramite_id = busqueda_por_memo(memo)[2]
        self.combo_origen.actualizar_items(catalogo_documentos(id_tramite=tramite_id))

    def filtrar_subtipos(self):
        self.combo_subtipos.actualizar_items(catalogo_subtipos(self.combo_tipos.currentData()))

    def mostrar_tipo_origen(self):
        self.label_origen.setText("Tipo Documento Origen: --")
        info_doc = busqueda_info_documento(self.combo_origen.currentData())
        if info_doc is not None:
            tipo_origen = catalogo_tipos(info_doc[2])[0]
            subtipo_origen = ("","")
            if info_doc[3] is not None:
                subtipo_origen = catalogo_subtipos(info_doc[2], info_doc[3])[0]
            self.label_origen.setText(f'Tipo Documento Origen: {tipo_origen[1]} {subtipo_origen[1]}')
        else:
            return

    def adjuntar_documento(self):
        tramite = busqueda_por_memo(self.combo_memos.currentData())[2]
        codigo_documento = self.line_codigo.text()
        fecha_documento = self.date_fecha.date().toString("yyyy-MM-dd")
        tipo = self.combo_tipos.currentData()
        subtipo = self.combo_subtipos.currentData()
        origen = self.combo_origen.currentData()
        resultado = anadir_documento_manual(tramite, codigo_documento, fecha_documento,
                                            tipo, subtipo, origen)
        
        QMessageBox.information(
            self,
            "Adjuntado Correctamente",
            f"El documento ha sido adjuntado correctamente"
        )