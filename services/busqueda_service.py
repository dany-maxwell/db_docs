from services.db_helper import ejecutar_query

def busqueda_por_memo(id_memo):
    query = "select * from v_info_tramite_por_memo where id = %s"
    return ejecutar_query(query, (id_memo,), fetch_one=True)

def busqueda_id_memo_por_documento(id_documento):
    query = """
        select mem.id from documento mem
        join tramite t on mem.tramite_id = t.id
        where t.id = (select t.id from tramite t
            join documento d on t.id = d.tramite_id
            where d.id = %s)
        and mem.tipo_documento_id = 1
    """
    result = ejecutar_query(query, (id_documento,), fetch_one=True)
    return result[0] if result else None

def busqueda_info_documento(id_documento):
    query= "select id, codigo_final, tipo_documento_id, subtipo_documento_id, fecha_documento, documento_origen_id from documento where id = %s"
    params = [id_documento]
    return ejecutar_query(query, params, fetch_one=True)

def busqueda_documentos_avanzada(
    memo=None,
    proveedor=None,
    unidad=None,
    tipo=None,
    subtipo=None,
    estado=None,
    codigo=None,
    fecha_desde=None,
    fecha_hasta=None,
    archivado=None
):
    query = "select * from v_busqueda_avanzada where 1=1"
    params = []

    filtros = [
        (memo, " and memo_id = %s"),
        (proveedor, " and proveedor_id = %s"),
        (unidad, " and unidad_id = %s"),
        (tipo, " and tipo_id = %s"),
        (subtipo, " and subtipo_id = %s"),
        (estado, " and estado = %s"),
        (codigo, " and codigo ilike %s"),
        (fecha_desde, " and fecha >= %s"),
        (fecha_hasta, " and fecha <= %s"),
        (archivado, " and archivado = %s"),
    ]

    for valor, condicion in filtros:
        if valor:
            query += condicion
            params.append(f"%{valor}%" if "ilike" in condicion else valor)

    query += " order by documento_id desc"
    return ejecutar_query(query, params, fetch_all=True)

def busqueda_info_proveedor(id_proveedor):
    query = "select * from proveedor where id = %s"
    return ejecutar_query(query, (id_proveedor,), fetch_one=True)

def busqueda_documento_origen(id_documento):
    query = "select * from documento where id = %s"
    return ejecutar_query(query, (id_documento,), fetch_one=True)
