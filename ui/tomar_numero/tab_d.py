from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGroupBox)

from ui.widgets import (
    MemoComboBox,
    OrigenComboBox)

from services.catalogo_service import (
    catalogo_documentos)

from services.busqueda_service import (
    busqueda_por_memo,
    busqueda_id_memo_por_documento)

from services.numeracion_service import crear_documento_con_numeracion

class TabDictamen(QWidget):
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

        box_ai = QGroupBox("Acto de Inicio Correspondiente")
        lay_ai = QVBoxLayout()

        ai_items = catalogo_documentos(6)
        self.combo_ai = OrigenComboBox(ai_items)
        lay_ai.addWidget(self.combo_ai)

        box_ai.setLayout(lay_ai)
        layout.addWidget(box_ai)

        self.button_tomar_numero = QPushButton("Tomar Numero IAP")
        layout.addWidget(self.button_tomar_numero)

        self.setLayout(layout)

        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_ai)
        self.combo_ai.currentIndexChanged.connect(self.filtrar_mem)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.label_proveedor.setText("")
            return
        proveedor = busqueda_por_memo(id_memo)[0]

        self.label_proveedor.setText(proveedor)

    def filtrar_ai (self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            new_items = catalogo_documentos(6)
        else:
            tramite = busqueda_por_memo(id_memo)[2]
            new_items = catalogo_documentos(6, None, tramite)
            
        self.combo_ai.currentIndexChanged.disconnect(self.filtrar_mem)
        self.combo_ai.actualizar_items(new_items)
        self.combo_ai.currentIndexChanged.connect(self.filtrar_mem)

    def filtrar_mem (self):
        id_tramite = self.combo_ai.currentData()
        id_memo = busqueda_id_memo_por_documento(id_tramite)
        self.combo_memos.currentIndexChanged.disconnect(self.filtrar_ai)
        self.combo_memos.actualizar_index(id_memo)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_ai)

    def tomar_numero(self):
        id_memo = self.combo_memos.currentData()
        id_origen = self.combo_ai.currentData()
        resultado = crear_documento_con_numeracion(
            tramite_id=busqueda_por_memo(id_memo)[2],
            tipo_documento_id=8,
            subtipo_documento_id=None,
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
