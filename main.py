import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

app = QApplication(sys.argv)

ventana = MainWindow()
ventana.show()

sys.exit(app.exec())