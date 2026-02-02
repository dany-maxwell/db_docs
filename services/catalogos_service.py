from db.connection import get_connection

# -------------------------------------------
# proveedores y unidades
# -------------------------------------------

def obtener_proveedores():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, nombre from proveedor order by nombre")

    datos = cur.fetchall()
    con.close()

    return datos


def obtener_unidades():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, nombre from unidad order by nombre")

    datos = cur.fetchall()
    con.close()

    return datos

# -------------------------------------------
# tipos y subtipos
# -------------------------------------------

def obtener_tipos():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id, nombre from tipo_documento order by nombre")

    datos = cur.fetchall()
    cur.close()
    con.close()

    return datos


def obtener_subtipos(tipo):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select id, nombre 
        from subtipo_documento
        where tipo_documento_id = %s 
        order by nombre
    """, (tipo,))

    datos = cur.fetchall()
    cur.close()
    con.close()

    return datos


# -------------------------------------------
# tramites
# -------------------------------------------

def obtener_tramites():
    con = get_connection()
    cur = con.cursor()

    cur.execute("select id from tramite order by id desc")

    datos = cur.fetchall()

    cur.close()
    con.close()

    return datos


# -------------------------------------------
# infracciones
# -------------------------------------------

def obtener_infracciones():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select id, codigo_infraccion 
        from infraccion 
        order by id
    """)

    datos = cur.fetchall()

    cur.close()
    con.close()

    return datos
