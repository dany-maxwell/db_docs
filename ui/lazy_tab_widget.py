"""
Widget que implementa lazy loading para tabs.
Los tabs se crean bajo demanda para mejorar el tiempo de carga inicial.
"""
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer


class LazyTabWidget(QTabWidget):
    """
    QTabWidget que carga tabs bajo demanda.
    Los tabs solo se crean cuando se hace clic en ellos.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_factories = {}      # {index: callable_factory}
        self._loaded_tabs = set()     # indices de tabs ya cargados
        self._tab_titles = {}         # {index: title}
        self.tabBarClicked.connect(self._on_tab_clicked)
    
    def add_lazy_tab(self, factory, title):
        """
        Añade un tab con lazy loading.
        
        Args:
            factory: Callable que retorna el widget del tab cuando se llame
            title: Título del tab
        """
        index = self.count()
        # Crear widget placeholder con el título
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(f"Cargando {title}...")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        self.addTab(placeholder, title)
        self._tab_factories[index] = factory
        self._tab_titles[index] = title
    
    def _on_tab_clicked(self, index):
        """Se ejecuta cuando se hace click en un tab."""
        if index not in self._loaded_tabs and index in self._tab_factories:
            self._load_tab(index)
    
    def _load_tab(self, index):
        """Carga el tab con un pequeño delay para permitir que la UI se actualice."""
        if index in self._loaded_tabs or index not in self._tab_factories:
            return
        
        # Usar QTimer para permitir que Qt procese eventos antes de cargar
        QTimer.singleShot(10, lambda: self._do_load_tab(index))
    
    def _do_load_tab(self, index):
        """Realiza la carga actual del tab."""
        if index < 0 or index >= self.count() or index in self._loaded_tabs:
            return
        
        try:
            factory = self._tab_factories[index]
            widget = factory()
            title = self.tabText(index)
            self.removeTab(index)
            self.insertTab(index, widget, title)
            self._loaded_tabs.add(index)
        except Exception as e:
            print(f"Error al cargar tab {index}: {e}")
            import traceback
            traceback.print_exc()
    
    def load_all_tabs(self):
        """Carga todos los tabs de forma síncrona."""
        for index in range(self.count()):
            if index not in self._loaded_tabs:
                self._do_load_tab(index)
    
    def get_tab_widget(self, index):
        """
        Obtiene el widget del tab, cargándolo si es necesario.
        
        Args:
            index: Índice del tab
            
        Returns:
            El widget del tab o None si no existe
        """
        if index < 0 or index >= self.count():
            return None
        
        if index not in self._loaded_tabs and index in self._tab_factories:
            self._do_load_tab(index)
        
        return self.widget(index) if index in self._loaded_tabs else None
    
    def load_first_tab_sync(self):
        """Carga el primer tab de forma síncrona al inicio."""
        if self.count() > 0 and 0 not in self._loaded_tabs:
            self._do_load_tab(0)
            self.setCurrentIndex(0)
