from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QMessageBox
from services.auditoria_service import crear_proveedor

class NuevoProveedor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Añadir nuevo Proveedor")
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        
        box_form = QGroupBox('Datos del "Proveedor"')
        form_lay = QVBoxLayout()

        form_lay.addWidget(QLabel("Nombre:"))
        self.text_nombre = QLineEdit()
        self.text_nombre.setObjectName("Nombre")
        form_lay.addWidget(self.text_nombre)

        form_lay.addWidget(QLabel("Cedula / Ruc:"))
        self.text_cedula_ruc = QLineEdit()
        self.text_cedula_ruc.setObjectName("Cedula/Ruc")
        form_lay.addWidget(self.text_cedula_ruc)
        
        form_lay.addWidget(QLabel("Canton:"))
        self.text_canton = QLineEdit()
        self.text_canton.setObjectName("Canton")
        form_lay.addWidget(self.text_canton)
        
        form_lay.addWidget(QLabel("Ciudad:"))
        self.text_ciudad = QLineEdit()
        self.text_ciudad.setObjectName("Ciudad")
        form_lay.addWidget(self.text_ciudad)
        
        form_lay.addWidget(QLabel("Provincia:"))
        self.text_provincia = QLineEdit()
        self.text_provincia.setObjectName("Provincia")
        form_lay.addWidget(self.text_provincia)
        
        box_form.setLayout(form_lay)
        layout.addWidget(box_form)

        self.button_nuevo = QPushButton('Añadir Nuevo Proveedor')
        layout.addWidget(self.button_nuevo)
        
        self.datos = {'Nombre' : self.text_nombre,
                      'Cedula / Ruc' : self.text_cedula_ruc,
                      'Canton' : self.text_canton,
                      'Ciudad' : self.text_ciudad,
                      'Provincia' : self.text_provincia}
        self.button_nuevo.clicked.connect(self.crear_nuevo_proveedor)

    def crear_nuevo_proveedor(self):
        for nombre_dato, dato in self.datos.items():
            if not dato.text().strip():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Campo requerido")
                msg.setText(f"El campo '{nombre_dato}' no puede estar vacío.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                return 

        resultado = crear_proveedor(
            nombre=self.datos['Nombre'].text().upper(),
            cedula=self.datos['Cedula / Ruc'].text(),
            canton=self.datos['Canton'].text().upper(),
            ciudad=self.datos['Ciudad'].text().upper(),
            provincia=self.datos['Provincia'].text().upper()
        )
        
        QMessageBox.information(
            self,
            'Proveedor añadido',
            f"Añadido \nNuevo Nombre: {resultado[0]} \nNueva Cedula / Ruc: {resultado[1]}"
        )
        self.close()

        self.datos['Nombre'].clear()
        self.datos['Cedula / Ruc'].clear()
        self.datos['Canton'].clear()
        self.datos['Ciudad'].clear()
        self.datos['Provincia'].clear()
        
        
            