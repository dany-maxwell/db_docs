from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.lazy_tab_widget import LazyTabWidget
from .tab_mem import TabMem
from .tab_ap import TabActuacionPrevia
from .tab_iap import TabInformeAP
from .tab_pr import TabProvidencia
from .tab_ai import TabActoInicio
from .tab_ij import TabInformeJuridico
from .tab_d import TabDictamen
from .tab_rpas import TabResolucion


class WidgetTomarNumero(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.tabs = LazyTabWidget()

        # Añadir tabs con lazy loading
        self.tabs.add_lazy_tab(TabMem, "(provicional)")
        self.tabs.add_lazy_tab(TabActuacionPrevia, "Actuación Previa")
        self.tabs.add_lazy_tab(TabInformeAP, "Informe AP")
        self.tabs.add_lazy_tab(TabProvidencia, "Providencias")
        self.tabs.add_lazy_tab(TabActoInicio, "Acto de Inicio")
        self.tabs.add_lazy_tab(TabInformeJuridico, "Informe Juridico")
        self.tabs.add_lazy_tab(TabDictamen, "Dictamen")
        self.tabs.add_lazy_tab(TabResolucion, "Resolución")

        layout.addWidget(self.tabs)

        self.setLayout(layout)
    
    def actualizar_combos(self):
        for i in range(self.tabs.count()):
            tab = self.tabs.get_tab_widget(i)
            if tab:
                if hasattr(tab, 'filtrar_origen_custom'):
                    tab.filtrar_origen_custom()
                if hasattr(tab, 'actualizar_combos'):
                    tab.actualizar_combos()