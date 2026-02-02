from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QLineEdit,
    QMessageBox
)

from services.catalogos_service import (
    obtener_tramites,
    obtener_tipos,
    obtener_subtipos,
)

from services.documentos_service import (obtener_tramite_por_codigo_documento, buscar_documentos_por_texto, obtener_actuaciones_previas)

from services.numeracion_service import crear_documento_con_numeracion


class TomarNumeroWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.tramite_actual = None

        layout = QVBoxLayout()

        # ============================
        layout.addWidget(QLabel("Tipo de documento a generar"))

        self.combo_tipo = QComboBox()
        layout.addWidget(self.combo_tipo)

        # ============================
        layout.addWidget(QLabel("Buscar por Memo o cualquier documento"))

        self.txt_buscar = QLineEdit()
        layout.addWidget(self.txt_buscar)

        self.combo_resultados = QComboBox()
        layout.addWidget(self.combo_resultados)

        # ============================
        layout.addWidget(QLabel("Actuación Previa correspondiente"))

        self.combo_ap = QComboBox()
        layout.addWidget(self.combo_ap)

        # ============================
        self.btn = QPushButton("Tomar Número")
        layout.addWidget(self.btn)

        self.setLayout(layout)

        # eventos
        self.txt_buscar.textChanged.connect(self.autocompletar)
        self.combo_resultados.currentIndexChanged.connect(self.cargar_ap)
        self.btn.clicked.connect(self.tomar_numero)

        self.cargar_tipos()

    # ---------------------------------

    def cargar_tipos(self):
        tipos = obtener_tipos()

        for t in tipos:
            nombre = t[1]

            # ❌ excluir
            if nombre in ["Memo Inicio P", "Peticion Razonada"]:
                continue

            self.combo_tipo.addItem(nombre, t[0])

    # ---------------------------------

    def autocompletar(self):
        texto = self.txt_buscar.text()

        if len(texto) < 3:
            return

        datos = buscar_documentos_por_texto(texto)

        self.combo_resultados.clear()

        for d in datos:
            self.combo_resultados.addItem(
                d[1],      # codigo visible
                int(d[2])  # 👈 FORZAR INT
            )

    # ---------------------------------

    def cargar_ap(self):

        tramite = self.combo_resultados.currentData()

        print("VALOR DEL COMBO:", tramite, type(tramite))

        if tramite is None:
            return

        # 👇 FORZAMOS a int real
        tramite = int(tramite)

        self.tramite_actual = tramite

        aps = obtener_actuaciones_previas(tramite)

        print("APS encontradas:", aps)

        self.combo_ap.clear()

        if not aps:
            self.combo_ap.addItem("No existen actuaciones previas", None)
            return

        for ap in aps:
            self.combo_ap.addItem(ap[1], ap[0])



    # ---------------------------------

    def tomar_numero(self):
        if not self.tramite_actual:
            QMessageBox.warning(
                self, "Atención",
                "Debe seleccionar un trámite primero"
            )
            return

        resultado = crear_documento_con_numeracion(
            tramite_id=self.tramite_actual,
            tipo_documento_id=self.combo_tipo.currentData(),
            subtipo_documento_id=None,
            codigo_manual=None,
            unidad_codigo="CZO2"
        )

        QMessageBox.information(
            self,
            "Número tomado",
            f"Código: {resultado['codigo']}\n"
            f"Fecha: {resultado['fecha']}"
        )
