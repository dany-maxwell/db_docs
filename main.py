import sys, os
import time
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    start = time.time()
    app = QApplication(sys.argv)

    window = MainWindow()

    window.setMinimumSize(900, 600)
    window.resize(1100, 700)

    window.show()
    print('tiempo de carga: ', time.time() - start)


    sys.exit(app.exec())


if __name__ == "__main__":
    main()
