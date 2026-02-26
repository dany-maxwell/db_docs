"""Clase base para tabs de tomar número"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QGroupBox, QSizePolicy
from ui.widgets import MemoComboBox
from services.catalogo_service import catalogo_documentos
from services.busqueda_service import busqueda_por_memo, busqueda_id_memo_por_documento
from services.auditoria_service import crear_documento_con_numeracion
from constants import UNIDAD_CODIGO_DEFAULT, MSG_NUMERO_TOMADO


class BaseTabDocumento(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self._setup_memo_box()
        self.setLayout(self.layout)
        self._filtrar_origen_custom_connected = False

    def _on_filtrar_origen_custom(self):
        self.filtrar_origen_custom()
    
    def _setup_memo_box(self):
        box_memo = QGroupBox("Memorando de Petición de PAS")
        lay_memo = QVBoxLayout()
        
        self.combo_memos = MemoComboBox(
            [(None, "- Sin Seleccionar -")] + catalogo_documentos(1)
        )
        self.combo_memos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lay_memo.addWidget(self.combo_memos)
        lay_memo.addWidget(QLabel("Proveedor:"))
        
        self.label_proveedor = QLabel("")
        lay_memo.addWidget(self.label_proveedor)
        box_memo.setLayout(lay_memo)
        self.layout.addWidget(box_memo)
        
        self.combo_memos.currentIndexChanged.connect(self.mostrar_proveedor)
    
    def mostrar_proveedor(self):
        id_memo = self.combo_memos.currentData()
        if not id_memo:
            self.label_proveedor.setText("")
            return
        proveedor = busqueda_por_memo(id_memo)[0]
        self.label_proveedor.setText(proveedor)
    
    def filtrar_origen(self, tipo_doc_id, subtipo_doc_id=None):
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
        id_tramite = self.combo_origen.currentData()
        if not id_tramite:
            return
        id_memo = busqueda_id_memo_por_documento(id_tramite)

        idx_origen = self.combo_origen.currentIndex()
        self.combo_memos.blockSignals(True)
        self.combo_memos.actualizar_index(id_memo)
        self.combo_memos.blockSignals(False)

        self.mostrar_proveedor()

        if idx_origen >= 0:
            self.combo_origen.setCurrentIndex(idx_origen)
    
    def filtrar_origen_custom(self):
        pass

    def actualizar_combos(self):
        self.combo_memos._setup_items([(None, "- Sin Seleccionar -")] + catalogo_documentos(1))
        self.filtrar_origen_custom()
        self.actualizar_combos_extra()

    def actualizar_combos_extra(self):
        pass
    
    def crear_documento(self, tipo_documento_id, subtipo_documento_id=None, 
                       documento_origen_id=None, asunto=None):
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
            unidad_codigo=UNIDAD_CODIGO_DEFAULT,
            asunto=asunto
        )
        
        QMessageBox.information(
            self,
            MSG_NUMERO_TOMADO,
            f"Código: {resultado['codigo']}\nFecha: {resultado['fecha']}"
        )
        return resultado
