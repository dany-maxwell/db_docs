from services.db_helper import ejecutar_query
from functools import lru_cache


def catalogo_proveedores():
    return ejecutar_query("select id, nombre from proveedor order by nombre", fetch_all=True)


def catalogo_unidades():
    return ejecutar_query("select id, codigo from unidad order by id", fetch_all=True)

def catalogo_servicios():
    return ejecutar_query("select id, nombre from servicio order by nombre", fetch_all=True)

def catalogo_documentos(id_tipo, id_subtipo=None, id_tramite=None):
    query = "select id, codigo_final from documento where tipo_documento_id = %s"
    params = [id_tipo]

    if id_subtipo is not None:
        query += " and subtipo_documento_id = %s"
        params.append(id_subtipo)

    if id_tramite is not None:
        query += " and tramite_id = %s"
        params.append(id_tramite)

    query += " order by id desc"
    return ejecutar_query(query, params, fetch_all=True)

def catalogo_documentos_tramite(id_tramite):
    query = """
        select codigo_final, tipo, subtipo, fecha_documento, documento_id
        from v_documentos_tramite
        where tramite_id = %s
        order by documento_id asc
    """
    return ejecutar_query(query, (id_tramite,), fetch_all=True)

def catalogo_reporte():
    return ejecutar_query("select * from v_reporte_tramites", fetch_all=True)

@lru_cache(maxsize=32)
def catalogo_tipos():
    return ejecutar_query("select id, nombre from tipo_documento", fetch_all=True)

@lru_cache(maxsize=128)
def catalogo_subtipos(id_tipo):
    return ejecutar_query(
        "select id, nombre from subtipo_documento where tipo_documento_id = %s",
        (id_tipo,),
        fetch_all=True
    )

@lru_cache(maxsize=32)
def catalogo_infracciones():
    return ejecutar_query("select id, codigo_infraccion from infraccion", fetch_all=True)
