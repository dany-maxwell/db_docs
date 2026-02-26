import sys, os
import time
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Carpeta temporal de PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def cargar_estilos(app):
    ruta_qss = resource_path("ui/styles/styles.qss")

    if os.path.exists(ruta_qss):
        with open(ruta_qss, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print("Error")

def main():
    start = time.time()
    app = QApplication(sys.argv)

    cargar_estilos(app)

    window = MainWindow()

    window.setMinimumSize(900, 600)
    window.resize(1100, 700)

    window.show()
    print('tiempo de carga: ', time.time() - start)


    sys.exit(app.exec())


if __name__ == "__main__":
    main()
