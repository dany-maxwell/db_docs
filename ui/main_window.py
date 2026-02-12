from PySide6.QtWidgets import QMainWindow, QTabWidget

from db.pg_listener import PgNotifyListener
from ui.crear_tramite.widget_crear_tramite import WidgetCrearTramite
from ui.tomar_numero.widget_tomar_numero import WidgetTomarNumero
from ui.consultar.widget_consultar import WidgetConsultar
from ui.inpugnacion.widget_impugnacion import WidgetImpugnacion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Numeración")
        self.resize(900, 600)

        self.tabs = QTabWidget()

        self.tabs.addTab(WidgetCrearTramite(), "Crear Trámite")
        self.tabs.addTab(WidgetTomarNumero(), "Tomar Número")
        self.tabs.addTab(WidgetConsultar(), "Consultar")
        self.tabs.addTab(WidgetImpugnacion(), "Impugnación")

        self.setCentralWidget(self.tabs)

        self.pg_listener = PgNotifyListener(
            channel="canal_documentos" 
        )
        self.pg_listener.notify_received.connect(self.on_db_update)
        self.pg_listener.start()
    
    def on_db_update(self, payload):
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, 'actualizar_combos'):
                widget.actualizar_combos()
            
