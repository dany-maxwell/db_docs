from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

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

        self.tabs = QTabWidget()

        self.tabs.addTab(TabMem(), "(provicional)")
        self.tabs.addTab(TabActuacionPrevia(), "Actuación Previa")
        self.tabs.addTab(TabInformeAP(), "Informe AP")
        self.tabs.addTab(TabProvidencia(), "Providencias")
        self.tabs.addTab(TabActoInicio(), "Acto de Inicio")
        self.tabs.addTab(TabInformeJuridico(), "Informe Juridico")
        self.tabs.addTab(TabDictamen(), "Dictamen")
        self.tabs.addTab(TabResolucion(), "Resolución")

        layout.addWidget(self.tabs)

        self.setLayout(layout)
    
    def actualizar_combos(self):
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, 'filtrar_origen_custom'):
                tab.filtrar_origen_custom()
            if hasattr(tab, 'actualizar_combos'):
                tab.actualizar_combos()