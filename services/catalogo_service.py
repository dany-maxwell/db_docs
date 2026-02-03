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

def catalogo_memorando_inicio_pas():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, codigo_final from documento where tipo_documento_id = 1 order by id desc;")

    datos = cur.fetchall()
    con.close()

    return datos

def catalogo_documentos(id_tipo, id_tramite = None) :
    con = get_connection()
    cur = con.cursor()

    if id_tramite == None:
        cur.execute("select id, codigo_final from documento where tipo_documento_id = %s order by id desc;", (id_tipo,))
    else:
        cur.execute("""select id, codigo_final from documento
                        where tipo_documento_id = %s 
                        and tramite_id = %s
                        order by id desc
                    """, (id_tipo, id_tramite))

    datos = cur.fetchall()
    con.close()

    return datos