from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox)

from ui.widgets import MemoComboBox

from services.catalogo_service import catalogo_documentos
from services.busqueda_service import (
    busqueda_por_memo)

from services.numeracion_service import crear_documento_con_numeracion

class TabActuacionPrevia(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Memorando de Peticion de PAS"))
        items = catalogo_documentos(1)
        self.combo_memos = MemoComboBox(items)
        layout.addWidget(self.combo_memos)

        layout.addWidget(QLabel("Proveedor:"))
        self.label_proveedor = QLabel("")
        layout.addWidget(self.label_proveedor)

        self.button_tomar_numero = QPushButton("Tomar Numero AP")
        layout.addWidget(self.button_tomar_numero)

        self.setLayout(layout)    

        self.combo_memos.currentIndexChanged.connect(self.id_memorando)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

    def id_memorando(self):
        id_memo = self.combo_memos.currentData()
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
        