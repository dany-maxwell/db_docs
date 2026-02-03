from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

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

        tabs = QTabWidget()

        tabs.addTab(TabActuacionPrevia(), "Actuación Previa")
        tabs.addTab(TabInformeAP(), "Informe AP")
        tabs.addTab(TabProvidencia(), "Providencias")
        tabs.addTab(TabActoInicio(), "Acto de Inicio")
        tabs.addTab(TabInformeJuridico(), "Informe Juridico")
        tabs.addTab(TabDictamen(), "Dictamen")
        tabs.addTab(TabResolucion(), "Resolución")

        layout.addWidget(tabs)

        self.setLayout(layout)
