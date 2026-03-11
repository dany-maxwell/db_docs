from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QVBoxLayout, QListWidget,
                                QCompleter, QMessageBox, QLabel, QPushButton, QWidget,
                                QLineEdit, QGridLayout, QGroupBox, QDateEdit, QRadioButton)
from PySide6.QtCore import Qt, QDate

from services.catalogo_service import (
    catalogo_documentos, catalogo_proveedores, catalogo_unidades, catalogo_tipos)
from constants import MSG_INFRACCION_AGREGADA, ESTADOS_COMBO

class BaseComboBox(QComboBox):
    DEFAULT_INDEX = -1
    PLACEHOLDER = "Buscar opción..."
    
    def __init__(self, items_with_ids=None, parent=None, with_completer=True):
        super().__init__(parent)
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.setMinimumContentsLength(20)
        self.setMaximumWidth(400)
        self.setEditable(True)
        self.with_completer = with_completer
        if items_with_ids:
            self._setup_items(items_with_ids)
        self.lineEdit().setPlaceholderText(self.PLACEHOLDER)
        self.setCurrentIndex(self.DEFAULT_INDEX)
    
    def _setup_items(self, items):
        if not items:
            return
        self.blockSignals(True)
        self.clear()
        
        codigos = [item[1] for item in items]
        for id_valor, codigo in items:
            self.addItem(codigo, id_valor)

        self.lineEdit().setPlaceholderText(self.PLACEHOLDER)
        self.setCurrentIndex(self.DEFAULT_INDEX)

        if self.with_completer:
            completer = QCompleter(codigos, self)
            completer.setFilterMode(Qt.MatchContains)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setCompletionMode(QCompleter.PopupCompletion)
            self.setCompleter(completer)
        
        self.blockSignals(False)
    
    def actualizar_items(self, nuevos_items):
        self.clear()
        self._setup_items(nuevos_items)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.showPopup()

class MemoComboBox(BaseComboBox):
    DEFAULT_INDEX = 0
    
    def actualizar_index(self, id_tramite):
        self.setCurrentIndex(self.findData(id_tramite))

class OrigenComboBox(BaseComboBox):
    pass

class TipoComboBox(BaseComboBox):
    pass

class SubtipoComboBox(BaseComboBox):
    PLACEHOLDER = "No hay subtipos"

class InfraccionComboBox(BaseComboBox):
    pass

class CatalogoComboBox(BaseComboBox):
    pass

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
        if id_inf and id_inf not in self.ids_seleccionados:
            self.ids_seleccionados.append(id_inf)
            self.lista.addItem(self.combo.currentText())
        elif id_inf in self.ids_seleccionados:
            QMessageBox.warning(self, "Aviso", MSG_INFRACCION_AGREGADA)

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
        layout.addWidget(widget)
        self.widget = widget

class SelectorFechaMes(QGroupBox):
    def __init__(self):
        super().__init__("Periodo de Resolución")
        layout = QHBoxLayout(self)
        self.edit_fecha = QDateEdit(QDate.currentDate())
        self.edit_fecha.setCalendarPopup(True)
        self.combo_mes = QComboBox()
        for i in range(1, 13):
            self.combo_mes.addItem(str(i), i)
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
        self.combo_memo = MemoComboBox([(None, "")] + catalogo_documentos(1))
        self.combo_prov = CatalogoComboBox(catalogo_proveedores())
        self.combo_unid = CatalogoComboBox(catalogo_unidades())
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Ej: PAS-2023...")

        campos_bus = [
            ("Memo:", self.combo_memo),
            ("Proveedor:", self.combo_prov),
            ("Unidad:", self.combo_unid),
            ("Código:", self.txt_codigo)
        ]
        for i, (txt, widget) in enumerate(campos_bus):
            lay_bus.addWidget(QLabel(txt), i, 0)
            lay_bus.addWidget(widget, i, 1)

        self.box_fil = QGroupBox("Filtros")
        lay_fil = QGridLayout(self.box_fil)
        self.combo_tipo = TipoComboBox(catalogo_tipos())
        self.combo_tipo.setEditable(False)
        self.combo_sub = SubtipoComboBox([])
        self.combo_sub.setEditable(False)
        self.combo_est = QComboBox()
        self.combo_est.addItems(ESTADOS_COMBO)
        self.date_desde = QDateEdit(QDate.currentDate().addYears(-10))
        self.date_hasta = QDateEdit(QDate.currentDate().addDays(1))
        for d in [self.date_desde, self.date_hasta]:
            d.setCalendarPopup(True)

        campos_fil = [
            ("Tipo:", self.combo_tipo),
            ("Subtipo:", self.combo_sub),
            ("Estado:", self.combo_est),
            ("Desde:", self.date_desde),
            ("Hasta:", self.date_hasta)
        ]
        for i, (txt, widget) in enumerate(campos_fil):
            lay_fil.addWidget(QLabel(txt), i, 0)
            lay_fil.addWidget(widget, i, 1)

        self.btn_limpiar = QPushButton("Limpiar filtros")
        layout.addWidget(self.box_bus)
        layout.addWidget(self.box_fil)
        layout.addWidget(self.btn_limpiar)
    
    def actualizar_combos(self):
        self.combo_memo._setup_items([(None, "")] + catalogo_documentos(1))
        self.combo_prov._setup_items(catalogo_proveedores())

    def obtener_filtros(self):
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

        self.blockSignals(True)
        for combo in self.findChildren(QComboBox):
            combo.setCurrentIndex(-1)
        for edit in self.findChildren(QLineEdit):
            edit.clear()
        self.combo_est.setCurrentIndex(0)
        self.blockSignals(False)

class RadioCustom(QRadioButton):
    def mousePressEvent(self, event):
        if self.isChecked():
            self.setAutoExclusive(False)
            self.setChecked(False)
            self.setAutoExclusive(True)
        else:
            super().mousePressEvent(event)