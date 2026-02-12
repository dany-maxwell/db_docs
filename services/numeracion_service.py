from services.db_helper import ejecutar_query

def crear_tramite(
    proveedor_id,
    unidad_id,
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
    query = "select crear_tramite(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    result = ejecutar_query(
        query,
        (proveedor_id, unidad_id, estado, fecha_tramite, asunto, 
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
    unidad_codigo,
    codigo_manual=None,
    subtipo_documento_id=None,
    documento_origen_id=None
):
    query = "select crear_documento(%s, %s, %s, %s, %s, %s)"
    result = ejecutar_query(
        query,
        (tramite_id, tipo_documento_id, subtipo_documento_id,
         documento_origen_id, codigo_manual, unidad_codigo),
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

def agregar_infraccion(doc_id, infraccion_id):
    print(f"Agregando infracción {infraccion_id} al documento {doc_id}")
    query = "select agregar_infraccion_a_documento(%s, %s)"
    ejecutar_query(query, (doc_id, infraccion_id), commit=True)
