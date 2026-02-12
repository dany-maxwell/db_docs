import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def cargar_estilos(app):
    ruta_estilos = Path(__file__).parent / "ui" / "styles" / "styles.qss"
    with open(ruta_estilos, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cargar_estilos(app)
    
    ventana = MainWindow()
    ventana.show()
    
    sys.exit(app.exec())
