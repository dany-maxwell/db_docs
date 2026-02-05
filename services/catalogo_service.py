from db.connection import get_connection

def catalogo_proveedores():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, nombre from proveedor order by nombre")

    datos = cur.fetchall()
    con.close()

    return datos


def catalogo_unidades():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, nombre from unidad order by id")

    datos = cur.fetchall()
    con.close()

    return datos

def catalogo_documentos(id_tipo, id_subtipo = None, id_tramite = None) :
    con = get_connection()
    cur = con.cursor()

    query = """
        select id, codigo_final
        from documento
        where tipo_documento_id = %s
    """

    params = [id_tipo]

    if id_subtipo is not None:
        query += " and subtipo_documento_id = %s"
        params.append(id_subtipo)

    if id_tramite is not None:
        query += " and tramite_id = %s"
        params.append(id_tramite)

    query += " order by id desc"

    cur.execute(query, params)

    datos = cur.fetchall()
    con.close()

    return datos

def catalogo_tipos():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, nombre from tipo_documento")

    datos = cur.fetchall()
    con.close()

    return datos

def catalogo_subtipos(id_tipo):
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, nombre from subtipo_documento where tipo_documento_id = %s", (id_tipo,))

    datos = cur.fetchall()
    con.close()

    return datos

def catalogo_infracciones():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, codigo_infraccion from infraccion")

    datos = cur.fetchall()
    con.close()

    return datos