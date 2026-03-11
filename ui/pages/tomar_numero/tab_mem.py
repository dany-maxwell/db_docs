from PySide6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout, QMessageBox, QRadioButton, QHBoxLayout, QTextEdit
from .base_tab import BaseTabDocumento

from services.busqueda_service import busqueda_por_memo
from services.auditoria_service import actualizar_estado, añadir_observacion

from ui.widgets.widgets import RadioExclusivoDeseleccionable

class TabMem(BaseTabDocumento):
    def __init__(self):
        super().__init__()
        self.ui()
    
    def ui(self):
        self.box_estado = QGroupBox()
        self.layout_estado = QVBoxLayout()

        self.lay_h = QHBoxLayout()
        self.radio_devolver = RadioExclusivoDeseleccionable("¿Devuelve el memo?")
        self.radio_requiereap = RadioExclusivoDeseleccionable("¿Requiere Actuación Previa?")
        self.lay_h.addWidget(self.radio_devolver)
        self.lay_h.addWidget(self.radio_requiereap)
        self.layout_estado.addLayout(self.lay_h)

        self.text_razon = QTextEdit()
        self.text_razon.setPlaceholderText("Razón de la devolución o requerimiento")
        self.layout_estado.addWidget(self.text_razon)

        self.acceptar_btn = QPushButton("Aceptar")
        self.layout_estado.addWidget(self.acceptar_btn)

        self.box_estado.setLayout(self.layout_estado)

        self.box_trmite = QGroupBox("Cerrar Caso")
        self.layout_tramite = QVBoxLayout()
        self.btn_cerrar = QPushButton("Cerrar Trámite")
        self.layout_tramite.addWidget(self.btn_cerrar)

        self.box_trmite.setLayout(self.layout_tramite)
        self.layout.addWidget(self.box_estado)

        self.layout.addWidget(self.box_trmite)

        self.acceptar_btn.clicked.connect(self.acceptar_memo)
        self.btn_cerrar.clicked.connect(self.finalizar_tramite)

    def acceptar_memo(self):
        id_tramite = busqueda_por_memo(self.combo_memos.currentData())[2]
        if self.radio_devolver.isChecked():
            actualizar_estado(6, id_tramite)
        elif self.radio_requiereap.isChecked():
            actualizar_estado(2, id_tramite)
    
        añadir_observacion(self.text_razon.toPlainText(), id_tramite)
        QMessageBox.information(self, "Éxito", "El memo ha sido procesado exitosamente.")
    
    def finalizar_tramite(self):
        id_tramite = busqueda_por_memo(self.combo_memos.currentData())[2]
        actualizar_estado(6, id_tramite)
        QMessageBox.information(self, "Éxito", "El trámite ha sido cerrado exitosamente.")
        

    