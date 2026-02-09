import sys
from PySide6.QtWidgets import ( QComboBox, 
                                QCompleter)
from PySide6.QtCore import Qt

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