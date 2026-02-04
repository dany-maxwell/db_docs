from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QPushButton, QGroupBox, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem)

class WidgetConsultar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        box_busqueda = QGroupBox("Búsqueda por Memo")
        lay_bus = QHBoxLayout()

        self.txt_memo = QLineEdit()
        self.txt_memo.setPlaceholderText("Escriba el MEMO INICIO P")

        self.btn_buscar = QPushButton("Buscar")

        lay_bus.addWidget(QLabel("Memo:"))
        lay_bus.addWidget(self.txt_memo)
        lay_bus.addWidget(self.btn_buscar)

        box_busqueda.setLayout(lay_bus)

        box_info = QGroupBox("Datos del Trámite")
        lay_info = QVBoxLayout()

        self.lbl_proveedor = QLabel("Proveedor: ---")
        self.lbl_unidad = QLabel("Unidad: ---")
        self.lbl_estado = QLabel("Estado: ---")
        self.lbl_fecha = QLabel("Fecha: ---")

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

        self.btn_buscar.clicked.connect(self.buscar)

    def buscar(self):

        memo = self.txt_memo.text()

        if not memo:
            return

        # --- AQUÍ luego irá tu service real ---

        # SIMULADO
        self.lbl_proveedor.setText("Proveedor: CNT EP")
        self.lbl_unidad.setText("Unidad: CZO2")
        self.lbl_estado.setText("Estado: En instrucción")
        self.lbl_fecha.setText("Fecha: 2025-03-12")

        # cargar tabla fake
        self.cargar_tabla([
            ("ACTUACIÓN PREVIA", "", "AP-CZO2-2025-0001", "2025-03-01", "", ""),
            ("ACTO DE INICIO", "", "AI-CZO2-2025-0005", "2025-03-05", "AP-0001", "117 a)1"),
            ("PROVIDENCIA", "APERTURA", "PR-0003", "2025-03-07", "AI-0005", "")
        ])
    
    def cargar_tabla(self, datos):

        self.tabla.setRowCount(0)

        for fila in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)

            for col, valor in enumerate(fila):
                self.tabla.setItem(
                    row, col,
                    QTableWidgetItem(str(valor))
                )


