from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout,
                                QLineEdit, QDateEdit, QPushButton, QTextEdit, QMessageBox)
from PySide6.QtCore import QDate

from ui.widgets.widgets import CatalogoComboBox
from services.catalogo_service import catalogo_unidades, catalogo_proveedores, catalogo_servicios
from services.busqueda_service import busqueda_info_proveedor
from services.auditoria_service import crear_tramite
from constants import ESTADO_POR_DEFECTO, FORMATO_FECHA, MSG_TRAMITE_INICIADO

from .widget_nuevo_proveedor import NuevoProveedor

class WidgetCrearTramite(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.nueva_ventana = None
        self.button_add_prov.clicked.connect(self.abrir_form_nuevo)
        self.combo_proveedores.currentIndexChanged.connect(self.mostrar_datos_proveedor)
        self.button_iniciar_tramite.clicked.connect(self.iniciar_tramite)

    def setup_ui(self):
        layout = QVBoxLayout()
        
        box_proveedor = QGroupBox("Selecciona Proveedor")
        lay_prov = QVBoxLayout()
        lay_prob_ad = QHBoxLayout()

        self.combo_proveedores = CatalogoComboBox(catalogo_proveedores())
        self.button_add_prov = QPushButton('Añadir "Proveedor"')

        lay_prob_ad.addWidget(self.combo_proveedores)
        lay_prob_ad.addWidget(self.button_add_prov, 0)

        self.labels_prov = {
            "nombre": QLabel("Nombre: -"),
            "cedula": QLabel("Cédula/Ruc: -"),
            "ciudad": QLabel("Ciudad: -"),
            "canton": QLabel("Canton: -"),
            "provincia": QLabel("Provincia: -")
        }
        lay_prov.addLayout(lay_prob_ad)
        for label in self.labels_prov.values():
            lay_prov.addWidget(label)
        box_proveedor.setLayout(lay_prov)
        layout.addWidget(box_proveedor)
        
        box_datos = QGroupBox("Datos")
        lay_datos = QVBoxLayout()
        
        lay_unidad = QHBoxLayout()
        lay_unidad.addWidget(QLabel("Unidad: "))
        self.combo_unidad = CatalogoComboBox(catalogo_unidades())
        lay_unidad.addWidget(self.combo_unidad)
        lay_datos.addLayout(lay_unidad)
        
        lay_servicio = QHBoxLayout()
        lay_servicio.addWidget(QLabel("Servicio: "))
        self.combo_servicio = CatalogoComboBox(catalogo_servicios())
        lay_servicio.addWidget(self.combo_servicio)
        lay_datos.addLayout(lay_servicio)
        box_datos.setLayout(lay_datos)
        
        box_tramite = QGroupBox("Trámite")
        lay_tramite = QVBoxLayout()
        
        self.docs = {}
        for cod, etiqueta in [("memo", "Memorando Inicio PAS: "),
                               ("peticion", "Peticion Razonada: "),
                               ("informe", "Informe Técnico: ")]:
            lay = QHBoxLayout()
            lay.addWidget(QLabel(etiqueta))
            self.docs[cod] = {"line": QLineEdit(), "date": QDateEdit()}
            self.docs[cod]["date"].setCalendarPopup(True)
            self.docs[cod]["date"].setDate(QDate.currentDate())
            lay.addWidget(self.docs[cod]["line"])
            lay.addWidget(self.docs[cod]["date"])
            lay_tramite.addLayout(lay)
        
        lay_asunto = QVBoxLayout()
        lay_asunto.addWidget(QLabel("Asunto: "))
        self.line_asunto = QTextEdit()
        lay_asunto.addWidget(self.line_asunto)
        lay_tramite.addLayout(lay_asunto)
        box_tramite.setLayout(lay_tramite)
        
        layout.addWidget(box_datos)
        layout.addWidget(box_tramite)
        
        self.button_iniciar_tramite = QPushButton(" Iniciar Trámite")
        layout.addWidget(self.button_iniciar_tramite)
        self.setLayout(layout)

    def abrir_form_nuevo(self):
        if self.nueva_ventana is None:
            self.nueva_ventana = NuevoProveedor()
            self.nueva_ventana.show()
        else:
            self.nueva_ventana.activateWindow()
            self.nueva_ventana.raise_()
            self.nueva_ventana.show()

    def mostrar_datos_proveedor(self):
        id_proveedor = self.combo_proveedores.currentData()
        if not id_proveedor:
            for label in self.labels_prov.values():
                label.setText("-")
            return
        
        datos = busqueda_info_proveedor(id_proveedor)
        if datos:
            self.labels_prov["nombre"].setText(f"Nombre: {datos[1]}")
            self.labels_prov["cedula"].setText(f"Cédula/Ruc: {datos[2]}")
            self.labels_prov["ciudad"].setText(f"Ciudad: {datos[4]}")
            self.labels_prov["canton"].setText(f"Canton: {datos[3]}")
            self.labels_prov["provincia"].setText(f"Provincia: {datos[5]}")

    def actualizar_proveedores(self):
        self.actualizar_combos()

    def actualizar_combos(self):
        self.combo_proveedores._setup_items(catalogo_proveedores())
        self.combo_unidad._setup_items(catalogo_unidades())
        self.docs["memo"]["line"].clear()
        self.docs["memo"]["date"].setDate(QDate.currentDate())
        self.docs["peticion"]["line"].clear()
        self.docs["peticion"]["date"].setDate(QDate.currentDate())
        self.docs["informe"]["line"].clear()
        self.docs["informe"]["date"].setDate(QDate.currentDate())
        self.line_asunto.clear()

    def iniciar_tramite(self):
        codigo_informe = self.docs["informe"]["line"].text().strip()
        codigo_peticion = self.docs["peticion"]["line"].text().strip()
        
        resultado = crear_tramite(
            proveedor_id=self.combo_proveedores.currentData(),
            unidad_id=self.combo_unidad.currentData(),
            servicio_id=self.combo_servicio.currentData(),
            estado=ESTADO_POR_DEFECTO,
            fecha_tramite=QDate.currentDate().toString(FORMATO_FECHA),
            asunto=self.line_asunto.toPlainText(),
            codigo_memo=self.docs["memo"]["line"].text(),
            fecha_memo=self.docs["memo"]["date"].date().toString(FORMATO_FECHA),
            codigo_peticion=codigo_peticion if codigo_peticion else None,
            fecha_peticion=self.docs["peticion"]["date"].date().toString(FORMATO_FECHA),
            codigo_informe=codigo_informe if codigo_informe else None,
            fecha_informe=self.docs["informe"]["date"].date().toString(FORMATO_FECHA)
        )

        QMessageBox.information(
            self,
            MSG_TRAMITE_INICIADO,
            f"Trámite iniciado con éxito.\nCódigo de Memorando: {resultado[1]}\nFecha: {resultado[2]}"
        )