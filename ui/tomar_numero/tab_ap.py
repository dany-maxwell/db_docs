from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGroupBox)

from ui.widgets import MemoComboBox

from services.catalogo_service import catalogo_documentos
from services.busqueda_service import (
    busqueda_por_memo)

from services.numeracion_service import crear_documento_con_numeracion

class TabActuacionPrevia(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        box_memo = QGroupBox("Memorando de Petición de PAS")
        lay_memo = QVBoxLayout()

        self.combo_memos = MemoComboBox([(None, "- Sin Seleccionar -")] + catalogo_documentos(1))
        lay_memo.addWidget(self.combo_memos)

        lay_memo.addWidget(QLabel("Proveedor:"))
        self.label_proveedor = QLabel("")
        lay_memo.addWidget(self.label_proveedor)

        box_memo.setLayout(lay_memo)
        layout.addWidget(box_memo)

        self.button_tomar_numero = QPushButton("Tomar Numero AP")
        layout.addWidget(self.button_tomar_numero)

        self.setLayout(layout)    

        self.combo_memos.currentIndexChanged.connect(self.id_memorando)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

    def id_memorando(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.label_proveedor.setText("")
            return
        proveedor = busqueda_por_memo(id_memo)[0]

        self.label_proveedor.setText(proveedor)

    def tomar_numero(self):
        id_memo = self.combo_memos.currentData()
        resultado = crear_documento_con_numeracion(
            tramite_id=busqueda_por_memo(id_memo)[2],
            tipo_documento_id=4,
            subtipo_documento_id=None,
            codigo_manual=None,
            unidad_codigo=busqueda_por_memo(id_memo)[1]
        )

        QMessageBox.information(
            self,
            "Número tomado",
            f"Código: {resultado['codigo']}\n"
            f"Fecha: {resultado['fecha']}"
        )
        