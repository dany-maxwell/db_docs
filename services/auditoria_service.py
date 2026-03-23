from services.db_helper import ejecutar_query

def crear_tramite(
    proveedor_id,
    unidad_id,
    servicio_id,
    estado,
    fecha_tramite,
    asunto,
    codigo_memo,
    fecha_memo,
    codigo_peticion=None,
    fecha_peticion=None,
    codigo_informe=None,
    fecha_informe=None
):
    query = "select crear_tramite(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    result = ejecutar_query(
        query,
        (proveedor_id, unidad_id, servicio_id, estado, fecha_tramite, asunto, 
         codigo_memo, fecha_memo, codigo_peticion, fecha_peticion, 
         codigo_informe, fecha_informe),
        fetch_one=True,
        commit=True
    )
    tramite_id = result[0]

    query2 = "select codigo_final, fecha_documento from documento where tramite_id = %s and tipo_documento_id = 1"
    codigo_memo_generado, fecha_memo_generada = ejecutar_query(query2, (tramite_id,), fetch_one=True)

    return {
        "tramite_id": tramite_id,
        "codigo_memo": codigo_memo_generado,
        "fecha_memo": fecha_memo_generada
    }


def crear_documento_con_numeracion(
    tramite_id,
    tipo_documento_id,
    unidad_codigo=None,
    codigo_manual=None,
    fecha_documento=None,
    subtipo_documento_id=None,
    documento_origen_id=None,
    asunto=None,
    plazo=None,
    fecha_termino=None
):
    query = "select crear_documento(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    result = ejecutar_query(
        query,
        (tramite_id, tipo_documento_id, subtipo_documento_id,
         documento_origen_id, codigo_manual, unidad_codigo, fecha_documento, asunto, plazo, fecha_termino),
        fetch_one=True,
        commit=True
    )
    id_doc = result[0]

    query2 = "select codigo_final, fecha_documento from documento where id = %s"
    codigo_generado, fecha = ejecutar_query(query2, (id_doc,), fetch_one=True)

    return {
        "id": id_doc,
        "codigo": codigo_generado,
        "fecha": fecha
    }

def anadir_documento_manual(tramite, codigo, fecha, tipo, subtipo, origen):
    query = "call nuevo_documento(%s,%s,%s,%s,%s,%s)"
    ejecutar_query(query, (tramite, codigo, fecha, tipo, subtipo, origen), commit=True)
    
def agregar_infraccion(doc_id, infraccion_id):
    query = "select agregar_infraccion_a_documento(%s, %s)"
    ejecutar_query(query, (doc_id, infraccion_id), commit=True)

def aplicar_inpugnacion(codigo_impugnacion, fecha_impugnacion, tramite_id, documento_id):
    query = "select aplicar_impugnacion(%s, %s, %s, %s)"
    ejecutar_query(query, (codigo_impugnacion, fecha_impugnacion, tramite_id, documento_id), commit=True)

def prosigue_tramite (prosigue, tramite_id):
    query= "select prosigue_tramite(%s, %s)"
    ejecutar_query(query, (prosigue, tramite_id), commit=True)

def añadir_observacion(observacion, tramite_id):
    query= "update tramite set observacion = %s where id = %s"
    ejecutar_query(query, (observacion, tramite_id), commit=True)

def actualizar_estado (estado, tramite_id):
    estados = {
        1 : "PETICIÓN PAS PENDIENTE",
        2 : "REQUIERE ACTUACION PREVIA",
        3 : "EN ACTUACIÓN PREVIA",
        4 : "EN INSTRUCCIÓN",
        5 : "EN RESOLUCIÓN",
        6 : "RESUELTO"
    }

    estado_txt = estados.get(estado)
    query= "select actualizar_estado_tramite(%s, %s)"

    ejecutar_query(query, (estado_txt, tramite_id), commit=True)

def crear_proveedor(nombre, cedula, canton, ciudad, provincia):
    query="select nuevo_proveedor(%s, %s, %s, %s, %s)"
    result = ejecutar_query(query, (nombre, cedula, canton, ciudad, provincia),fetch_one=True, commit=True)
    
    proveedor_id = result
    query2="select nombre, cedula_ruc from proveedor where id = %s"
    n_nombre, n_cedula = ejecutar_query(query2, proveedor_id, fetch_one=True, commit=True)
    return n_nombre, n_cedula

def asignar_fecha_termino(fecha, plazo):
    query="select sumar_dias_laborables(%s, %s)"
    return ejecutar_query(query, (fecha, plazo), fetch_one=True)
