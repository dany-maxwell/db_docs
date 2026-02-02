import sys
from PySide6.QtWidgets import QApplication, QTabWidget, QMainWindow

from ui.crear_tramite import CrearTramiteWidget
from ui.tomar_numero import TomarNumeroWidget


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de Trámites")
        self.resize(900, 600)

        tabs = QTabWidget()

        tabs.addTab(CrearTramiteWidget(), "Crear Trámite")
        tabs.addTab(TomarNumeroWidget(), "Tomar Número")

        self.setCentralWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec())