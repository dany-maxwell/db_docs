from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QGroupBox, QTableWidget,
    QTableWidgetItem, QPushButton, QComboBox, QDateEdit, QGridLayout,
    QMessageBox, QFileDialog
)

from PySide6.QtCore import QTimer, QDate

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from services.busqueda_service import (
    busqueda_documentos_avanzada
)

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_tipos,
    catalogo_subtipos,
    catalogo_proveedores,
    catalogo_unidades
)

from ui.widgets import (
    MemoComboBox,
    TipoComboBox,
    SubtipoComboBox,
    CatalogoComboBox
)

class WidgetConsultar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        box_busqueda = QGroupBox("Búsqueda")
        lay_bus = QGridLayout()

        self.combo_memo = MemoComboBox(catalogo_documentos(1))
        lay_bus.addWidget(QLabel("Memo:"), 0, 0)
        lay_bus.addWidget(self.combo_memo, 0, 1)

        self.combo_proveedor = CatalogoComboBox(catalogo_proveedores())
        lay_bus.addWidget(QLabel("Proveedor:"), 1, 0)
        lay_bus.addWidget(self.combo_proveedor, 1, 1)

        self.combo_unidad = CatalogoComboBox(catalogo_unidades())
        lay_bus.addWidget(QLabel("Unidad:"), 2, 0)
        lay_bus.addWidget(self.combo_unidad, 2, 1)

        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Buscar por código...")
        lay_bus.addWidget(QLabel("Código:"), 3, 0)
        lay_bus.addWidget(self.txt_codigo, 3, 1)

        box_busqueda.setLayout(lay_bus)

        box_filtros = QGroupBox("Filtros")
        lay_fil = QGridLayout()

        self.combo_tipo = TipoComboBox(catalogo_tipos())
        self.combo_subtipo = SubtipoComboBox([])

        lay_fil.addWidget(QLabel("Tipo:"), 0, 0)
        lay_fil.addWidget(self.combo_tipo, 0, 1)

        lay_fil.addWidget(QLabel("Subtipo:"), 1, 0)
        lay_fil.addWidget(self.combo_subtipo, 1, 1)

        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["", "INICIADO", "En actuacion previa"])
        lay_fil.addWidget(QLabel("Estado:"), 2, 0)
        lay_fil.addWidget(self.combo_estado, 2, 1)

        self.date_desde = QDateEdit()
        self.date_desde.setCalendarPopup(True)
        self.date_desde.setDate(QDate.currentDate().addMonths(-1))

        self.date_hasta = QDateEdit()
        self.date_hasta.setCalendarPopup(True)
        self.date_hasta.setDate(QDate.currentDate())

        lay_fil.addWidget(QLabel("Fecha desde:"), 3, 0)
        lay_fil.addWidget(self.date_desde, 3, 1)

        lay_fil.addWidget(QLabel("Fecha hasta:"), 4, 0)
        lay_fil.addWidget(self.date_hasta, 4, 1)

        self.btn_limpiar = QPushButton("Limpiar filtros")
        lay_fil.addWidget(self.btn_limpiar, 5, 0, 1, 2)

        box_filtros.setLayout(lay_fil)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(10)

        self.tabla.setHorizontalHeaderLabels([
            "N° Trámite",
            "Proveedor",
            "Unidad",
            "Fecha inicio trámite",

            "Tipo",
            "Subtipo",
            "Código",
            "Fecha documento",
            "Origen",
            "Infracciones"
        ])


        layout.addWidget(box_busqueda)
        layout.addWidget(box_filtros)
        layout.addWidget(self.tabla)

        self.btn_excel = QPushButton("Exportar a Excel")
        self.btn_excel.clicked.connect(self.exportar_excel)

        layout.addWidget(self.btn_excel)

        self.setLayout(layout)

        self.cargar_tabla(busqueda_documentos_avanzada())

        self.timer_codigo = QTimer()
        self.timer_codigo.setSingleShot(True)
        self.timer_codigo.timeout.connect(self.buscar)

        self.txt_codigo.textChanged.connect(self.on_codigo_changed)

        self.combo_memo.currentIndexChanged.connect(self.buscar)
        self.combo_proveedor.currentIndexChanged.connect(self.buscar)
        self.combo_unidad.currentIndexChanged.connect(self.buscar)
        

        self.combo_tipo.currentIndexChanged.connect(self.actualizar_subtipos)
        self.combo_tipo.currentIndexChanged.connect(self.buscar)
        self.combo_subtipo.currentIndexChanged.connect(self.buscar)

        self.combo_estado.currentIndexChanged.connect(self.buscar)

        self.date_desde.dateChanged.connect(self.buscar)
        self.date_hasta.dateChanged.connect(self.buscar)

        

        self.btn_limpiar.clicked.connect(self.limpiar)

    def actualizar_subtipos(self):
        id_tipo = self.combo_tipo.currentData()
        self.combo_subtipo.actualizar_items(
            catalogo_subtipos(id_tipo)
        )

    def buscar(self):

        datos = busqueda_documentos_avanzada(
            memo=self.combo_memo.currentData(),
            proveedor=self.combo_proveedor.currentData(),
            unidad=self.combo_unidad.currentData(),

            codigo=self.txt_codigo.text(),

            tipo=self.combo_tipo.currentData(),
            subtipo=self.combo_subtipo.currentData(),

            estado=self.combo_estado.currentText(),

            fecha_desde=self.date_desde.date().toString("yyyy-MM-dd"),
            fecha_hasta=self.date_hasta.date().toString("yyyy-MM-dd")
        )

        self.cargar_tabla(datos)

    def on_codigo_changed(self):
        self.timer_codigo.start(500)

    def cargar_tabla(self, datos):

        self.tabla.setRowCount(0)

        for fila in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)

            map = {
                0: fila[0],
                1: fila[2],
                2: fila[4],
                3: fila[7],
                4: fila[10],
                5: fila[12],
                6: fila[14],
                7: fila[15],
                8: fila[16],
                9: fila[17],
            }

            for col, valor in map.items():
                self.tabla.setItem(
                    row, col,
                    QTableWidgetItem(str(valor if valor is not None else ""))
                )

    def limpiar(self):

        self.combo_memo.setCurrentIndex(-1)
        self.combo_proveedor.setCurrentIndex(-1)
        self.combo_unidad.setCurrentIndex(-1)

        self.txt_codigo.clear()

        self.combo_tipo.setCurrentIndex(-1)
        self.combo_subtipo.setCurrentIndex(-1)

        self.combo_estado.setCurrentIndex(0)

        self.buscar()

    def exportar_excel(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Excel",
            "consulta_tramites.xlsx",
            "Excel (*.xlsx)"
        )

        if not ruta:
            return

        wb = Workbook()

        id_memo = self.combo_memo.currentData()

        if id_memo:
            self._crear_hoja_resumen(wb)
            self._crear_hoja_documentos(wb, "Documentos")
        else:
            self._crear_hoja_documentos(wb, "Listado")

        wb.save(ruta)

        QMessageBox.information(self, "Exportado", "Excel generado correctamente")

    def _crear_hoja_resumen(self, wb):
        ws = wb.active
        ws.title = "Resumen"

        ws["A1"] = "RESUMEN DEL TRÁMITE"
        ws["A1"].font = Font(bold=True, size=14)

        if self.tabla.rowCount() == 0:
            ws["A3"] = "No hay datos cargados"
            return

        f = 0

        datos = [
            ("N° Trámite", self.tabla.item(f, 0).text()),
            ("Proveedor", self.tabla.item(f, 1).text()),
            ("Unidad", self.tabla.item(f, 2).text()),
            ("Fecha inicio", self.tabla.item(f, 3).text()),
        ]

        fila = 3
        for titulo, valor in datos:
            ws[f"A{fila}"] = titulo
            ws[f"B{fila}"] = valor
            ws[f"A{fila}"].font = Font(bold=True)
            fila += 1

        ws[f"A{fila+1}"] = "Total documentos:"
        ws[f"B{fila+1}"] = self.tabla.rowCount()

    def _crear_hoja_documentos(self, wb, nombre):
        ws = wb.create_sheet(nombre)

        headers = [
            "N° Trámite",
            "Proveedor",
            "Unidad",
            "Fecha Inicio",
            "Tipo",
            "Subtipo",
            "Código",
            "Fecha Documento",
            "Origen",
            "Infracciones"
        ]

        ws.append(headers)

        for col in range(1, len(headers)+1):
            ws.cell(1, col).font = Font(bold=True)

        for row in range(self.tabla.rowCount()):
            fila = []

            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(row, col)
                fila.append(item.text() if item else "")

            ws.append(fila)

        for column_cells in ws.columns:
            length = max(len(str(cell.value or "")) for cell in column_cells)
            ws.column_dimensions[column_cells[0].column_letter].width = length + 2
