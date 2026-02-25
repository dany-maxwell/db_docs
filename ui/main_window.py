from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer
from db.pg_listener import PgNotifyListener
from ui.lazy_tab_widget import LazyTabWidget
from ui.crear_tramite.widget_crear_tramite import WidgetCrearTramite
from ui.tomar_numero.widget_tomar_numero import WidgetTomarNumero
from ui.consultar.widget_consultar import WidgetConsultar
from ui.inpugnacion.widget_impugnacion import WidgetImpugnacion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Numeración")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)

        self.tabs = LazyTabWidget()

        # Añadir tabs con lazy loading
        self.tabs.add_lazy_tab(WidgetCrearTramite, "Crear Trámite")
        self.tabs.add_lazy_tab(WidgetTomarNumero, "Tomar Número")
        self.tabs.add_lazy_tab(WidgetConsultar, "Consultar")
        self.tabs.add_lazy_tab(WidgetImpugnacion, "Impugnación")

        self.setCentralWidget(self.tabs)
        
        # Cargar el primer tab de forma sincrónica (para que esté listo al abrir)
        # Se ejecuta después de que la UI esté visible
        QTimer.singleShot(100, self._load_first_tab)

        self.pg_listener = PgNotifyListener(
            channel="canal_documentos" 
        )
        self.pg_listener.notify_received.connect(self.on_db_update)
        self.pg_listener.start()
    
    def _load_first_tab(self):
        """Carga el primer tab de forma sincrónica."""
        self.tabs.load_first_tab_sync()
    
    def on_db_update(self, payload):
        # Cargar todos los tabs antes de actualizar (si no están cargados)
        self.tabs.load_all_tabs()
        
        for i in range(self.tabs.count()):
            widget = self.tabs.get_tab_widget(i)
            if widget and hasattr(widget, 'actualizar_combos'):
                widget.actualizar_combos()
            
