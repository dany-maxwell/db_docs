from db.connection import get_connection

def obtener_tramite_por_codigo_documento(codigo):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select tramite_id, id, codigo_final, fecha_documento
        from documento
        where codigo_final = %s
    """, (codigo,))

    dato = cur.fetchone()

    cur.close()
    con.close()

    return dato

def obtener_documentos_por_tramite(tramite_id):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select 
            d.id,
            d.codigo_final,
            t.nombre as tipo,
            s.nombre as subtipo,
            d.fecha_documento
        from documento d
        join tipo_documento t 
            on d.tipo_documento_id = t.id
        left join subtipo_documento s 
            on d.subtipo_documento_id = s.id
        where d.tramite_id = %s
        order by d.id
    """, (tramite_id,))

    datos = cur.fetchall()

    cur.close()
    con.close()

    return datos

def buscar_documentos_por_texto(texto):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select id, codigo_final, tramite_id, tipo_documento_id
        from documento
        where codigo_final ilike %s
        order by codigo_final
        limit 20
    """, (f"%{texto}%",))

    datos = cur.fetchall()

    cur.close()
    con.close()

    return datos

def obtener_actuaciones_previas(tramite_id):
    print("TIPO RECIBIDO:", type(tramite_id), tramite_id)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        select id, codigo_final
        from documento
        where tramite_id = %s
        and tipo_documento_id in (
            select id from tipo_documento
            where nombre ilike '%%ACTUACIÓN PREVIA%%'
        )
        order by fecha_documento
    """, (tramite_id,))

    datos = cur.fetchall()

    cur.close()
    conn.close()

    return datos

