from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

from ui.widgets import (
    MemoComboBox,
    OrigenComboBox,
    TipoComboBox)

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_subtipos)

from services.busqueda_service import (
    busqueda_por_memo,
    busqueda_id_memo_por_documento
)

from services.numeracion_service import crear_documento_con_numeracion

class TabInformeJuridico(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Memorando de Petición de PAS"))
        memo_items = catalogo_documentos(1)
        self.combo_memos = MemoComboBox(memo_items)
        layout.addWidget(self.combo_memos)

        layout.addWidget(QLabel("Proveedor:"))
        self.label_proveedor = QLabel("")
        layout.addWidget(self.label_proveedor)

        layout.addWidget(QLabel("Tipo Informe Jurídico"))
        t_ij_items = catalogo_subtipos(11)
        self.combo_ij = TipoComboBox(t_ij_items)
        layout.addWidget(self.combo_ij)

        self.label_origen = QLabel("Acto de Inicio")
        items = catalogo_documentos(6)
        self.combo_origen = OrigenComboBox(items)
        layout.addWidget(self.label_origen)
        layout.addWidget(self.combo_origen)
        self.label_origen.hide()
        self.combo_origen.hide()

        self.button_tomar_numero = QPushButton("Tomar Numero IAP")
        layout.addWidget(self.button_tomar_numero)

        self.setLayout(layout)

        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_origen)
        self.combo_ij.currentIndexChanged.connect(self.mostrar_origen)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        proveedor = busqueda_por_memo(id_memo)[0]

        self.label_proveedor.setText(proveedor)

    def filtrar_origen (self):
        id_memo = self.combo_memos.currentData()
        tramite = busqueda_por_memo(id_memo)[2]
        new_items = catalogo_documentos(6, None, tramite)
        print(new_items)
        self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
        self.combo_origen.actualizar_items(new_items)
        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)

    def filtrar_mem (self):
        id_tramite = self.combo_origen.currentData()
        id_memo = busqueda_id_memo_por_documento(id_tramite)
        self.combo_memos.currentIndexChanged.disconnect(self.filtrar_origen)
        self.combo_memos.actualizar_index(id_memo)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_origen)

    def mostrar_origen (self):
        idx_tipo = self.combo_ij.currentIndex()
        if idx_tipo == 0:
            self.label_origen.show()
            self.combo_origen.show()
        else: 
            self.label_origen.hide()
            self.combo_origen.hide()

    def tomar_numero(self):
        id_memo = self.combo_memos.currentData()
        id_origen = self.combo_origen.currentData()
        if not id_origen: return None
        id_subtipo = self.combo_ij.currentData()
    
        resultado = crear_documento_con_numeracion(
            tramite_id=busqueda_por_memo(id_memo)[2],
            tipo_documento_id=11,
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