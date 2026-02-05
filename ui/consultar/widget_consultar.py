from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QGroupBox, QTableWidget,
    QTableWidgetItem, QPushButton
)

from PySide6.QtCore import QTimer

from services.busqueda_service import (
    buscar_documentos,
    busqueda_por_memo
)

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_tipos,
    catalogo_subtipos
)

from ui.widgets import (
    MemoComboBox,
    TipoComboBox,
    SubtipoComboBox
)


class WidgetConsultar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        box_busqueda = QGroupBox("Filtros de búsqueda")
        lay_bus = QHBoxLayout()

        memo_items = catalogo_documentos(1)
        self.combo_memo = MemoComboBox(memo_items)
        self.combo_memo.setPlaceholderText("Seleccione Memorando Inicio PAS")
        lay_bus.addWidget(QLabel("Memo:"))
        lay_bus.addWidget(self.combo_memo)

        self.text_codigo = QLineEdit()
        self.text_codigo.setPlaceholderText("Escriba código parcial")
        lay_bus.addWidget(QLabel("Código:"))
        lay_bus.addWidget(self.text_codigo)
    
        tipos_items = catalogo_tipos()
        self.combo_tipos = TipoComboBox(tipos_items)
        self.combo_tipos.setPlaceholderText("Tipo documento")
        lay_bus.addWidget(QLabel("Tipo:"))
        lay_bus.addWidget(self.combo_tipos)

        self.combo_subtipos = SubtipoComboBox([])
        self.combo_subtipos.setPlaceholderText("Subtipo")
        lay_bus.addWidget(QLabel("Subtipo:"))
        lay_bus.addWidget(self.combo_subtipos)

        self.btn_limpiar = QPushButton("Limpiar filtros")
        lay_bus.addWidget(self.btn_limpiar)

        self.btn_limpiar.clicked.connect(self.limpiar_filtros)


        box_busqueda.setLayout(lay_bus)

        box_info = QGroupBox("Datos del Trámite")
        lay_info = QVBoxLayout()

        self.lbl_tramite = QLabel("Id Tramite: ---")
        self.lbl_proveedor = QLabel("Proveedor: ---")
        self.lbl_unidad = QLabel("Unidad: ---")
        self.lbl_estado = QLabel("Estado: ---")
        self.lbl_fecha = QLabel("Fecha: ---")

        lay_info.addWidget(self.lbl_tramite)
        lay_info.addWidget(self.lbl_proveedor)
        lay_info.addWidget(self.lbl_unidad)
        lay_info.addWidget(self.lbl_estado)
        lay_info.addWidget(self.lbl_fecha)

        box_info.setLayout(lay_info)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)

        self.tabla.setHorizontalHeaderLabels([
            "Tipo",
            "Subtipo",
            "Código",
            "Fecha",
            "Origen",
            "Infracciones"
        ])

        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(box_busqueda)
        layout.addWidget(box_info)
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.cargar_tabla(buscar_documentos())

        self.combo_memo.currentIndexChanged.connect(self.aplicar_filtros)
        self.text_codigo.textChanged.connect(self.aplicar_filtros)
        self.combo_tipos.currentIndexChanged.connect(self.filtrar_subtipos)
        self.combo_tipos.currentIndexChanged.connect(self.aplicar_filtros)
        self.combo_subtipos.currentIndexChanged.connect(self.aplicar_filtros)

    def filtrar_subtipos(self):
        id_tipo = self.combo_tipos.currentData()
        new_items = catalogo_subtipos(id_tipo)

        self.combo_subtipos.actualizar_items(new_items)

    def aplicar_filtros(self):

        id_memo = self.combo_memo.currentData()
        texto_codigo = self.text_codigo.text().strip()

        id_tipo = self.combo_tipos.currentData()
        id_subtipo = self.combo_subtipos.currentData()

        if id_memo:
            info = busqueda_por_memo(id_memo)

            self.lbl_tramite.setText(f"Id Tramite: {info[2]}")
            self.lbl_proveedor.setText(f"Proveedor: {info[0]}")
            self.lbl_unidad.setText(f"Unidad: {info[1]}")
            self.lbl_estado.setText(f"Estado: {info[3]}")
            self.lbl_fecha.setText(f"Fecha de Inicio: {str(info[4])}")

        datos = buscar_documentos(
            memo=id_memo,
            codigo=texto_codigo,
            tipo=id_tipo,
            subtipo=id_subtipo
        )

        self.cargar_tabla(datos)

    def limpiar_filtros(self):

        self.combo_memo.setCurrentIndex(-1)
        self.text_codigo.clear()

        self.combo_tipos.setCurrentIndex(-1)
        self.combo_subtipos.actualizar_items([])

        self.lbl_tramite.setText("Id Tramite: ---")
        self.lbl_proveedor.setText("Proveedor: ---")
        self.lbl_unidad.setText("Unidad: ---")
        self.lbl_estado.setText("Estado: ---")
        self.lbl_fecha.setText("Fecha: ---")

        self.aplicar_filtros()

    def cargar_tabla(self, datos):

        self.tabla.setRowCount(0)

        for fila in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)

            for col, valor in enumerate(fila):
                self.tabla.setItem(
                    row, col,
                    QTableWidgetItem(str(valor or ""))
                )
