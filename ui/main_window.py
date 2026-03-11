from PySide6.QtWidgets import QMainWindow, QTabWidget
from db.pg_listener import PgNotifyListener
from ui.pages.crear_tramite.ui_crear_tramite import WidgetCrearTramite
from ui.pages.tomar_numero.ui_tomar_numero import WidgetTomarNumero
from ui.pages.consultar.ui_consultar import WidgetConsultar
from ui.pages.inpugnacion.ui_impugnacion import WidgetImpugnacion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Numeración")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)

        self.tabs = QTabWidget()

        self.tabs.addTab(WidgetCrearTramite(), "Crear Trámite")
        self.tabs.addTab(WidgetTomarNumero(), "Tomar Número")
        self.tabs.addTab(WidgetConsultar(), "Consultar")
        self.tabs.addTab(WidgetImpugnacion(), "Impugnación")

        self.setCentralWidget(self.tabs)

        self.pg_listener = PgNotifyListener(
            channel="canal_documentos" 
        )
        self.pg_listener_proveedores = PgNotifyListener(
            channel="canal_proveedores" 
        )
        self.pg_listener.notify_received.connect(self.on_db_update)
        self.pg_listener.start()

        self.pg_listener_proveedores.notify_received.connect(self.on_proveedores_update)
        self.pg_listener_proveedores.start()
    
    def on_db_update(self, payload):
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, 'actualizar_combos'):
                widget.actualizar_combos()

    def on_proveedores_update(self, payload):
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, 'actualizar_proveedores'):
                widget.actualizar_proveedores()
            
