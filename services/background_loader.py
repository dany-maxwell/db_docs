"""
Sistema de carga de datos en background para optimizar rendimiento.
Los datos se cargan en threads separados sin bloquear la UI.
"""
from PySide6.QtCore import QThread, Signal, QObject
import time


class DataLoaderThread(QThread):
    """Thread para cargar datos sin bloquear la UI."""
    
    data_loaded = Signal(str, object)  # key, data
    error_occurred = Signal(str, str)  # key, error_message
    
    def __init__(self, key, loader_func, *args, **kwargs):
        """
        Args:
            key: Identificador único del dato siendo cargado
            loader_func: Función que carga el dato
            args, kwargs: Argumentos para loader_func
        """
        super().__init__()
        self.key = key
        self.loader_func = loader_func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """Carga los datos en un thread separado."""
        try:
            data = self.loader_func(*self.args, **self.kwargs)
            self.data_loaded.emit(self.key, data)
        except Exception as e:
            self.error_occurred.emit(self.key, str(e))
            import traceback
            traceback.print_exc()


class BackgroundDataLoader(QObject):
    """
    Gestor central para cargar datos en background.
    Permite cachear resultados para evitar recargas innecesarias.
    """
    
    data_loaded = Signal(str, object)  # key, data
    
    def __init__(self):
        super().__init__()
        self._threads = {}        # {key: LoaderThread}
        self._cache = {}          # {key: data}
        self._cache_enabled = True
    
    def load_data(self, key, loader_func, *args, use_cache=True, **kwargs):
        """
        Carga datos de forma asincrónica.
        
        Args:
            key: Identificador único
            loader_func: Función que carga el dato
            use_cache: Si True, usa cache si está disponible
            args, kwargs: Argumentos para loader_func
        """
        # Retornar del cache si está disponible
        if use_cache and self._cache_enabled and key in self._cache:
            self.data_loaded.emit(key, self._cache[key])
            return
        
        # Evitar cargas duplicadas
        if key in self._threads:
            return
        
        # Crear thread de carga
        thread = DataLoaderThread(key, loader_func, *args, **kwargs)
        thread.data_loaded.connect(self._on_data_loaded)
        thread.error_occurred.connect(self._on_error)
        
        self._threads[key] = thread
        thread.start()
    
    def _on_data_loaded(self, key, data):
        """Se ejecuta cuando los datos se cargaron exitosamente."""
        self._cache[key] = data
        self.data_loaded.emit(key, data)
        
        # Limpiar thread
        if key in self._threads:
            del self._threads[key]
    
    def _on_error(self, key, error_msg):
        """Se ejecuta si hay error al cargar."""
        print(f"Error al cargar {key}: {error_msg}")
        if key in self._threads:
            del self._threads[key]
    
    def clear_cache(self, key=None):
        """Limpia el cache."""
        if key is None:
            self._cache.clear()
        elif key in self._cache:
            del self._cache[key]
    
    def set_cache(self, key, data):
        """Define manualmente un valor en el cache."""
        self._cache[key] = data


# Instancia global
_data_loader = None

def get_data_loader():
    """Obtiene la instancia global del cargador de datos."""
    global _data_loader
    if _data_loader is None:
        _data_loader = BackgroundDataLoader()
    return _data_loader
