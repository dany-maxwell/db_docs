from PySide6.QtWidgets import QMainWindow, QTabWidget

from ui.crear_tramite.widget_crear_tramite import WidgetCrearTramite
from ui.tomar_numero.widget_tomar_numero import WidgetTomarNumero
from ui.consultar.widget_consultar import WidgetConsultar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Numeración")
        self.resize(900, 600)

        tabs = QTabWidget()

        tabs.addTab(WidgetCrearTramite(), "Crear Trámite")
        tabs.addTab(WidgetTomarNumero(), "Tomar Número")
        tabs.addTab(WidgetConsultar(), "Consultar")

        self.setCentralWidget(tabs)
