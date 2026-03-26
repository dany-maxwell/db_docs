from db.connection import get_connection
from services.db_helper import ejecutar_query
from functools import lru_cache


def catalogo_proveedores():
    
    return ejecutar_query("select id, nombre from proveedor order by nombre", fetch_all=True)

def catalogo_unidades():
    return ejecutar_query("select id, codigo from unidad order by id", fetch_all=True)

def catalogo_servicios():
    return ejecutar_query("select id, servicio from servicio order by servicio", fetch_all=True)

def catalogo_documentos(id_tipo=None, id_subtipo=None, id_tramite=None, id_documento=None):
    query = "select id, codigo_final from documento where 1 = 1"
    params = []
    if id_tipo is not None:
        query += " and tipo_documento_id = %s"
        params.append(id_tipo)

    if id_subtipo is not None:
        query += " and subtipo_documento_id = %s"
        params.append(id_subtipo)

    if id_tramite is not None:
        query += " and tramite_id = %s"
        params.append(id_tramite)

    if id_documento is not None:
        query += " and id = %s"
        params.append(id_documento)

    query += " order by fecha_documento desc nulls last, id desc"
    return ejecutar_query(query, params, fetch_all=True) 

def catalogo_documentos_tramite(id_tramite, no_resueltos=False):
    query = """
        select codigo_final, tipo, subtipo, fecha_documento, documento_id
        from v_documentos_tramite
        where tramite_id = %s
    """
    params = [id_tramite]
    if no_resueltos:
        query += " and estado <> 'RESUELTO'"

    query += " order by fecha_documento asc nulls last, documento_id asc"
    return ejecutar_query(query, params, fetch_all=True)

def catalogo_reporte():
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("select * from vista_seguimiento_final")
            rows = cur.fetchall()
            columnas = [desc[0] for desc in cur.description]
    return {
        'rows': rows,
        'columnas': columnas
    }

@lru_cache(maxsize=32)
def catalogo_tipos(id=None):
    query = "select id, nombre from tipo_documento where 1=1"
    params = []
    if id is not None:
        query += " and id=%s"
        params.append(id)
    return ejecutar_query(query=query, params=params, fetch_all=True)

def catalogo_tipos_extra():
    return ejecutar_query("select id, nombre from tipo_documento where id in (12, 13, 14)", fetch_all=True)

@lru_cache(maxsize=128)
def catalogo_subtipos(id_tipo, id=None):
    query = "select id, nombre from subtipo_documento where tipo_documento_id = %s"
    params = [id_tipo]
    if id is not None:
        query+= " and id = %s"
        params.append(id)
    return ejecutar_query( query, params, fetch_all=True)

@lru_cache(maxsize=32)
def catalogo_infracciones():
    return ejecutar_query("select id, codigo_infraccion from infraccion", fetch_all=True)
