from PySide6.QtWidgets import ( QComboBox, QHBoxLayout, QVBoxLayout, QListWidget,
                                QCompleter, QMessageBox, QLabel, QPushButton, QWidget,
                                QLineEdit, QGridLayout )
from PySide6.QtCore import Qt

from services.catalogo_service import (
    catalogo_documentos,
    catalogo_proveedores,
    catalogo_unidades,
    catalogo_tipos)

class MemoComboBox(QComboBox):
    def __init__(self, items_with_ids, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        
        codigos = [item[1] for item in items_with_ids]
        
        for id_valor, codigo in items_with_ids:
            self.addItem(codigo, id_valor)
        
        self.lineEdit().setPlaceholderText("Buscar opción...")
        self.setCurrentIndex(-1)

        completer = QCompleter(codigos, self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.setCompleter(completer)

    def actualizar_index(self, id_tramite):
        index = self.findData(id_tramite)
        self.setCurrentIndex(index)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.showPopup()

class OrigenComboBox(QComboBox):
    def __init__(self, items_with_ids, parent=None):
        super().__init__(parent)
        self.setEditable(True)

        if items_with_ids == None:
            return
        
        codigos = [item[1] for item in items_with_ids]
        
        for id_valor, codigo in items_with_ids:
            self.addItem(codigo, id_valor)
        
        self.lineEdit().setPlaceholderText("Buscar opción...")
        self.setCurrentIndex(-1)

        completer = QCompleter(codigos, self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.setCompleter(completer)

    def actualizar_items(self, nuevos_items):
        self.clear()
        for id_valor, codigo in nuevos_items:
            self.addItem(codigo, id_valor)
                
        nuevo_modelo = [item[1] for item in nuevos_items]
        self.completer().model().setStringList(nuevo_modelo)
        self.setCurrentIndex(-1)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.showPopup()

class TipoComboBox(QComboBox):
    def __init__(self, items_with_ids, parent=None):
        super().__init__(parent)
        self.setEditable(True)

        if items_with_ids == None:
            return

        for id_valor, codigo in items_with_ids:
            self.addItem(codigo, id_valor)
        
        self.lineEdit().setPlaceholderText("Buscar opción...")
        self.setCurrentIndex(-1)

    def actualizar_items(self, nuevos_items):
        self.clear()
        for id_valor, codigo in nuevos_items:
            self.addItem(codigo, id_valor)
                
        self.setCurrentIndex(-1)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.showPopup()

class SubtipoComboBox(QComboBox):
    def __init__(self, items_with_ids, parent=None):
        super().__init__(parent)
        self.setEditable(True)

        if items_with_ids == None:
            return

        for id_valor, codigo in items_with_ids:
            self.addItem(codigo, id_valor)
        
        self.lineEdit().setPlaceholderText("No hay subtipos")
        self.setCurrentIndex(-1)

    def actualizar_items(self, nuevos_items):
        self.clear()
        for id_valor, codigo in nuevos_items:
            self.addItem(codigo, id_valor)
                
        self.setCurrentIndex(-1)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.showPopup()

class InfraccionComboBox(QComboBox):
    def __init__(self, items_with_ids, parent=None):
        super().__init__(parent)
        self.setEditable(True)

        codigos = [item[1] for item in items_with_ids]
        
        for id_valor, codigo in items_with_ids:
            self.addItem(codigo, id_valor)
        
        self.lineEdit().setPlaceholderText("Buscar opción...")
        self.setCurrentIndex(-1)

        completer = QCompleter(codigos, self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.setCompleter(completer)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.showPopup()

class SelectorInfracciones(QWidget):
    def __init__(self, items_callback):
        super().__init__()
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Posible Infracción"))
        self.combo = InfraccionComboBox(items_callback())
        layout.addWidget(self.combo)

        self.lista = QListWidget()
        layout.addWidget(self.lista)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Añadir Infracción")
        self.btn_del = QPushButton("Quitar Infracción")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_del)
        layout.addLayout(btn_layout)

        self.ids_seleccionados = []
        self.btn_add.clicked.connect(self.agregar)
        self.btn_del.clicked.connect(self.quitar)

    def agregar(self):
        id_inf = self.combo.currentData()
        if id_inf in self.ids_seleccionados:
            return QMessageBox.warning(self, "Aviso", "Ya agregada")
        
        if id_inf:
            self.ids_seleccionados.append(id_inf)
            self.lista.addItem(self.combo.currentText())

    def quitar(self):
        fila = self.lista.currentRow()
        if fila >= 0:
            self.lista.takeItem(fila)
            self.ids_seleccionados.pop(fila)

    def limpiar(self):
        self.ids_seleccionados.clear()
        self.lista.clear()

class LabeledWidget(QWidget):
    def __init__(self, label_text, widget):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(label_text))
        self.widget = widget
        layout.addWidget(self.widget)

class CatalogoComboBox(QComboBox):
    def __init__(self, items_with_ids, parent=None):
        super().__init__(parent)
        self.setEditable(True)

        codigos = [item[1] for item in items_with_ids]
        
        for id_valor, codigo in items_with_ids:
            self.addItem(codigo, id_valor)
        
        self.lineEdit().setPlaceholderText("Buscar opción...")
        self.setCurrentIndex(-1)

        completer = QCompleter(codigos, self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.setCompleter(completer)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.showPopup()

from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QDateEdit, QComboBox
from PySide6.QtCore import QDate

class SelectorFechaMes(QGroupBox):
    def __init__(self):
        super().__init__("Periodo de Resolución")
        layout = QHBoxLayout(self)
        self.edit_fecha = QDateEdit(QDate.currentDate())
        self.edit_fecha.setCalendarPopup(True)
        self.combo_mes = QComboBox()

        for i in range(1, 13): self.combo_mes.addItem(str(i), i)
        
        layout.addWidget(self.combo_mes)
        layout.addWidget(self.edit_fecha)

class FormularioBusqueda(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.box_bus = QGroupBox("Búsqueda")
        lay_bus = QGridLayout(self.box_bus)
        
        self.combo_memo = MemoComboBox(catalogo_documentos(1))
        self.combo_prov = CatalogoComboBox(catalogo_proveedores())
        self.combo_unid = CatalogoComboBox(catalogo_unidades())
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Ej: PAS-2023...")

        campos = [
            ("Memo:", self.combo_memo),
            ("Proveedor:", self.combo_prov),
            ("Unidad:", self.combo_unid),
            ("Código:", self.txt_codigo)
        ]
        for i, (txt, widget) in enumerate(campos):
            lay_bus.addWidget(QLabel(txt), i, 0)
            lay_bus.addWidget(widget, i, 1)

        self.box_fil = QGroupBox("Filtros")
        lay_fil = QGridLayout(self.box_fil)

        self.combo_tipo = TipoComboBox(catalogo_tipos())
        self.combo_sub = SubtipoComboBox([])
        self.combo_est = QComboBox()
        self.combo_est.addItems(["", "INICIADO", "En actuacion previa"])
        
        self.date_desde = QDateEdit(QDate.currentDate().addMonths(-1))
        self.date_hasta = QDateEdit(QDate.currentDate().addDays(1))
        for d in [self.date_desde, self.date_hasta]: d.setCalendarPopup(True)

        filtros = [
            ("Tipo:", self.combo_tipo), ("Subtipo:", self.combo_sub),
            ("Estado:", self.combo_est), ("Desde:", self.date_desde),
            ("Hasta:", self.date_hasta)
        ]
        for i, (txt, widget) in enumerate(filtros):
            lay_fil.addWidget(QLabel(txt), i, 0)
            lay_fil.addWidget(widget, i, 1)

        self.btn_limpiar = QPushButton("Limpiar filtros")
        layout.addWidget(self.box_bus)
        layout.addWidget(self.box_fil)
        layout.addWidget(self.btn_limpiar)

    def obtener_filtros(self):
        """Devuelve un diccionario con todos los valores actuales"""
        return {
            "memo": self.combo_memo.currentData(),
            "proveedor": self.combo_prov.currentData(),
            "unidad": self.combo_unid.currentData(),
            "codigo": self.txt_codigo.text(),
            "tipo": self.combo_tipo.currentData(),
            "subtipo": self.combo_sub.currentData(),
            "estado": self.combo_est.currentText(),
            "fecha_desde": self.date_desde.date().toString("yyyy-MM-dd"),
            "fecha_hasta": self.date_hasta.date().toString("yyyy-MM-dd")
        }

    def limpiar(self):
        self.blockSignals(True)
        
        for combo in self.findChildren(QComboBox):
            combo.setCurrentIndex(-1)
        
        for edit in self.findChildren(QLineEdit):
            edit.clear()
            
        self.combo_est.setCurrentIndex(0) 
        
        self.blockSignals(False)