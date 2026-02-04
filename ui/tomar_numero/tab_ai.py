from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QListWidget)

from ui.widgets import (
    MemoComboBox,
    OrigenComboBox,
    InfraccionComboBox)

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_infracciones)

from services.busqueda_service import (
    busqueda_por_memo,
    busqueda_id_memo_por_documento)

from services.numeracion_service import (
    crear_documento_con_numeracion,
    agregar_infraccion)

class TabActoInicio(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Memorando de Peticion de PAS"))
        memo_items = catalogo_documentos(1)
        self.combo_memos = MemoComboBox(memo_items)
        layout.addWidget(self.combo_memos)

        layout.addWidget(QLabel("Proveedor:"))
        self.label_proveedor = QLabel("")
        layout.addWidget(self.label_proveedor)

        layout.addWidget(QLabel("Informe FINAL de Actuacion Previa Correspondiente"))
        iap_items = catalogo_documentos(5, 2)
        self.combo_iap = OrigenComboBox(iap_items)
        layout.addWidget(self.combo_iap)

        layout.addWidget(QLabel("Posible Infraccion"))
        inf_items = catalogo_infracciones()
        self.combo_inf = InfraccionComboBox(inf_items)
        layout.addWidget(self.combo_inf)

        layout.addWidget(QLabel("Lista:"))
        self.list_inf = QListWidget()
        layout.addWidget(self.list_inf)

        self.button_añadir_infraccion = QPushButton("Añadir Infraccion")
        layout.addWidget(self.button_añadir_infraccion)

        self.button_quitar_infraccion = QPushButton("Quitar Infraccion")
        layout.addWidget(self.button_quitar_infraccion)

        self.button_tomar_numero = QPushButton("Tomar Numero AI")
        layout.addWidget(self.button_tomar_numero)

        self.setLayout(layout)

        self.infracciones_seleccionadas = []

        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_iap)
        self.combo_iap.currentIndexChanged.connect(self.filtrar_mem)
        self.button_añadir_infraccion.clicked.connect(self.agregar_infraccion)
        self.button_quitar_infraccion.clicked.connect(self.quitar_infraccion)
        self.button_tomar_numero.clicked.connect(self.tomar_numero)

    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        proveedor = busqueda_por_memo(id_memo)[0]

        self.label_proveedor.setText(proveedor)

    def filtrar_iap (self):
        id_memo = self.combo_memos.currentData()
        tramite = busqueda_por_memo(id_memo)[2]
        new_items = catalogo_documentos(5, 2, tramite)
        self.combo_iap.currentIndexChanged.disconnect(self.filtrar_mem)
        self.combo_iap.actualizar_items(new_items)
        self.combo_iap.currentIndexChanged.connect(self.filtrar_mem)

    def filtrar_mem (self):
        id_tramite = self.combo_iap.currentData()
        id_memo = busqueda_id_memo_por_documento(id_tramite)
        self.combo_memos.currentIndexChanged.disconnect(self.filtrar_iap)
        self.combo_memos.actualizar_index(id_memo)
        self.combo_memos.currentIndexChanged.connect(self.filtrar_iap)

    def agregar_infraccion(self):
        id_infraccion = self.combo_inf.currentData()
        texto = self.combo_inf.currentText()

        if not id_infraccion:
            return

        if id_infraccion in self.infracciones_seleccionadas:
            QMessageBox.warning(self, "Aviso", "Ya agregaste esa infracción")
            return

        self.infracciones_seleccionadas.append(id_infraccion)
        self.list_inf.addItem(texto)
    
    def quitar_infraccion(self):
        fila = self.list_inf.currentRow()

        if fila >= 0:
            self.list_inf.takeItem(fila)
            del self.infracciones_seleccionadas[fila]

    def tomar_numero(self):
        id_memo = self.combo_memos.currentData()
        id_origen = self.combo_iap.currentData()
        resultado = crear_documento_con_numeracion(
            tramite_id=busqueda_por_memo(id_memo)[2],
            tipo_documento_id=6,
            subtipo_documento_id=None,
            documento_origen_id=id_origen,
            codigo_manual=None,
            unidad_codigo=busqueda_por_memo(id_memo)[1]
        )

        for inf in self.infracciones_seleccionadas:
            agregar_infraccion(resultado["id"], inf)
        self.infracciones_seleccionadas.clear()
        self.lista.clear()

        QMessageBox.information(
            self,
            "Número tomado",
            f"Código: {resultado['codigo']}\n"
            f"Fecha: {resultado['fecha']}"
        )

        
