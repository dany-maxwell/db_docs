import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def cargar_estilos(app):
    with open("ui/styles/styles.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

app = QApplication(sys.argv)

cargar_estilos(app)

ventana = MainWindow()
ventana.show()

sys.exit(app.exec())