from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QMessageBox,
    QLineEdit
)

from services.catalogos_service import obtener_proveedores, obtener_unidades
from services.tramite_service import crear_tramite
from services.numeracion_service import crear_documento_con_numeracion


class CrearTramiteWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Proveedor"))
        self.combo_proveedor = QComboBox()
        layout.addWidget(self.combo_proveedor)

        layout.addWidget(QLabel("Unidad"))
        self.combo_unidad = QComboBox()
        layout.addWidget(self.combo_unidad)

        # ==========================
        layout.addWidget(QLabel("Código Memo Inicio P (OBLIGATORIO)"))
        self.txt_memo = QLineEdit()
        layout.addWidget(self.txt_memo)

        layout.addWidget(QLabel("Petición Razonada (opcional)"))
        self.txt_peticion = QLineEdit()
        layout.addWidget(self.txt_peticion)

        layout.addWidget(QLabel("Primer Informe Técnico (opcional)"))
        self.txt_informe = QLineEdit()
        layout.addWidget(self.txt_informe)

        # ==========================

        self.btn = QPushButton("Crear Trámite")
        layout.addWidget(self.btn)

        self.setLayout(layout)

        self.cargar_catalogos()

        self.btn.clicked.connect(self.crear)

    # ---------------------------------

    def cargar_catalogos(self):
        for p in obtener_proveedores():
            self.combo_proveedor.addItem(p[1], p[0])

        for u in obtener_unidades():
            self.combo_unidad.addItem(u[1], u[0])

    # ---------------------------------

    def crear(self):
        memo = self.txt_memo.text().strip()

        if not memo:
            QMessageBox.warning(
                self,
                "Validación",
                "El Memo Inicio P es obligatorio"
            )
            return

        try:
            proveedor = self.combo_proveedor.currentData()
            unidad = self.combo_unidad.currentData()

            # 1. crear tramite
            tramite_id = crear_tramite(
                proveedor_id=proveedor,
                unidad_id=unidad,
                estado="En actuacion previa"
            )

            # 2. crear memo obligatorio
            doc_id = crear_documento_con_numeracion(
                tramite_id=tramite_id,
                tipo_documento_id=1,   # 👈 luego lo mapeamos mejor
                subtipo_documento_id=None,
                codigo_manual=memo,
                unidad_codigo="CZO2"
            )

            # 3. opcionales
            if self.txt_peticion.text():
                crear_documento_con_numeracion(
                    tramite_id,
                    2,
                    None,
                    self.txt_peticion.text(),
                    "CZO2"
                )

            if self.txt_informe.text():
                crear_documento_con_numeracion(
                    tramite_id,
                    3,
                    None,
                    self.txt_informe.text(),
                    "CZO2"
                )

            QMessageBox.information(
                self,
                "Éxito",
                f"Trámite creado\nMemo: {memo}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
