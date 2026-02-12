"""Clase base para tabs de tomar número"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QGroupBox
from ui.widgets import MemoComboBox
from services.catalogo_service import catalogo_documentos
from services.busqueda_service import busqueda_por_memo, busqueda_id_memo_por_documento
from services.numeracion_service import crear_documento_con_numeracion
from constants import UNIDAD_CODIGO_DEFAULT, MSG_NUMERO_TOMADO


class BaseTabDocumento(QWidget):
    """Clase base compartida por todos los tabs de tomar número"""
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self._setup_memo_box()
        self.setLayout(self.layout)
        self._filtrar_origen_custom_connected = False

    def _on_filtrar_origen_custom(self):
        self.filtrar_origen_custom()
    
    def _setup_memo_box(self):
        """Crea la sección de Memorando común a todos los tabs"""
        box_memo = QGroupBox("Memorando de Petición de PAS")
        lay_memo = QVBoxLayout()
        
        self.combo_memos = MemoComboBox(
            [(None, "- Sin Seleccionar -")] + catalogo_documentos(1)
        )
        lay_memo.addWidget(self.combo_memos)
        lay_memo.addWidget(QLabel("Proveedor:"))
        
        self.label_proveedor = QLabel("")
        lay_memo.addWidget(self.label_proveedor)
        box_memo.setLayout(lay_memo)
        self.layout.addWidget(box_memo)
        
        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
    
    def mostrar_proveedor(self):
        """Muestra el proveedor del memorando seleccionado"""
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.label_proveedor.setText("")
            return
        proveedor = busqueda_por_memo(id_memo)[0]
        self.label_proveedor.setText(proveedor)
    
    def filtrar_origen(self, tipo_doc_id, subtipo_doc_id=None):
        """Filtra origen según el memo seleccionado y limpia si no hay documentos."""
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            new_items = catalogo_documentos(tipo_doc_id, subtipo_doc_id)
        else:
            tramite = busqueda_por_memo(id_memo)[2]
            new_items = catalogo_documentos(tipo_doc_id, subtipo_doc_id, tramite)
        self.combo_origen.currentIndexChanged.disconnect(self.filtrar_mem)
        self.combo_origen.actualizar_items(new_items)
        self.combo_origen.currentIndexChanged.connect(self.filtrar_mem)
    
    def filtrar_mem(self):
        """Filtra memo según origen seleccionado y mantiene selección de origen."""
        id_tramite = self.combo_origen.currentData()
        if not id_tramite:
            return
        id_memo = busqueda_id_memo_por_documento(id_tramite)
        # Guardar selección actual de combo_origen
        idx_origen = self.combo_origen.currentIndex()
        # Actualizar combo_memos sin desconectar señales
        self.combo_memos.blockSignals(True)
        self.combo_memos.actualizar_index(id_memo)
        self.combo_memos.blockSignals(False)
        # Actualizar proveedor explícitamente
        self.mostrar_proveedor()
        # Restaurar selección de combo_origen si es posible
        if idx_origen >= 0:
            self.combo_origen.setCurrentIndex(idx_origen)
    
    def filtrar_origen_custom(self):
        pass

    def actualizar_combos(self):
        self.combo_memos._setup_items([(None, "- Sin Seleccionar -")] + catalogo_documentos(1))
        self.filtrar_origen_custom()
        self.actualizar_combos_extra()

    def actualizar_combos_extra(self):
        """Hook para que los tabs hijos refresquen combos/lists secundarios."""
        pass
    
    def crear_documento(self, tipo_documento_id, subtipo_documento_id=None, 
                       documento_origen_id=None):
        """Crea un documento con numeración"""
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            QMessageBox.warning(self, "Error", "Selecciona un memorando")
            return None
        
        resultado = crear_documento_con_numeracion(
            tramite_id=busqueda_por_memo(id_memo)[2],
            tipo_documento_id=tipo_documento_id,
            subtipo_documento_id=subtipo_documento_id,
            documento_origen_id=documento_origen_id,
            codigo_manual=None,
            unidad_codigo=UNIDAD_CODIGO_DEFAULT
        )
        
        QMessageBox.information(
            self,
            MSG_NUMERO_TOMADO,
            f"Código: {resultado['codigo']}\nFecha: {resultado['fecha']}"
        )
        return resultado
