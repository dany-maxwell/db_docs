from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox)

from ui.widgets import (
    MemosComboBox,
    APComboBox)

from services.catalogo_service import (
    catalogo_memorando_inicio_pas,
    catalogo_documentos)

from services.busqueda_service import (
    busqueda_proveedor_por_memo,
    busqueda_tramite_por_memo)

from services.numeracion_service import crear_documento_con_numeracion

class TabInformeAP(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Memorando de Peticion de PAS"))
        memo_items = catalogo_documentos(1)
        self.combo_memos = MemosComboBox(memo_items)
        layout.addWidget(self.combo_memos)

        layout.addWidget(QLabel("Proveedor:"))
        self.label_proveedor = QLabel("")
        layout.addWidget(self.label_proveedor)

        layout.addWidget(QLabel("Actuacion Previa Correspondiente"))
        ap_items = catalogo_documentos(4)
        self.combo_ap = APComboBox(ap_items)
        layout.addWidget(self.combo_ap)

        self.button_tomar_numero = QPushButton("Tomar Numero IAP")
        layout.addWidget(self.button_tomar_numero)

        self.setLayout(layout)

        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_ap)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        proveedor = busqueda_proveedor_por_memo(id_memo)

        self.label_proveedor.setText(proveedor[1])

    def filtrar_ap (self):
        id_memo = self.combo_memos.currentData()
        tramite = busqueda_tramite_por_memo(id_memo)
        new_items = catalogo_documentos(4, tramite)
        self.combo_ap.actualizar_items(new_items)

    def tomar_numero(self):
        id_memo = self.combo_memos.currentData()
        id_origen = self.combo_ap.currentData()
        resultado = crear_documento_con_numeracion(
            tramite_id=busqueda_tramite_por_memo(id_memo),
            tipo_documento_id=5,
            subtipo_documento_id=None,
            codigo_manual=id_origen,
            unidad_codigo="CZO2"
        )

        QMessageBox.information(
            self,
            "Número tomado",
            f"Código: {resultado['codigo']}\n"
            f"Fecha: {resultado['fecha']}"
        )
