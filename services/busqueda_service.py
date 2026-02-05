from db.connection import get_connection

def busqueda_por_memo(id_memo):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
                select * from v_info_tramite_por_memo
                where id = %s;                
                """, (id_memo,))

    dato = cur.fetchone()
    con.close()

    return dato

def busqueda_id_memo_por_documento(id_documento):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
                select mem.id from documento mem
                join tramite t on mem.tramite_id = t.id
                where t.id = (select t.id from tramite t
				                join documento d on t.id = d.tramite_id
				                where d.id = %s)
                and mem.tipo_documento_id = 1; 
                """, (id_documento,))
    
    dato = cur.fetchone()
    
    con.close()
    return dato[0] if dato else None

def busqueda_documentos_por_tramite(id_tramite):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
                select 
                tipo,
                subtipo,
                codigo_final,
                fecha_documento,
                origen,
                infracciones,
                tipo_id,
                subtipo_id
                 from v_documentos_tramite where tramite_id = %s
                """, (id_tramite,))
    
    datos = cur.fetchall()
    con.close()

    return datos

def busqueda_documentos_por_codigo(texto, id_tipo = None, id_subtipo = None):
    con = get_connection()
    cur = con.cursor()
    
    query =    """
                select 
                tipo,
                subtipo,
                codigo_final,
                fecha_documento,
                origen,
                infracciones,
                tipo_id,
                subtipo_id
                 from v_busqueda_por_codigo where codigo_final ilike %s
                """
    params = [f'%{texto}%']

    if id_tipo is not None:
        query += " and tipo_id = %s"
        params.append(id_tipo)

    if id_subtipo is not None:
        query += " and tramite_id = %s"
        params.append(id_subtipo)

    query += " order by documento_id desc"

    cur.execute(query, params)
    
    datos = cur.fetchall()
    con.close()

    return datos

def buscar_documentos(memo=None, codigo=None, tipo=None, subtipo=None):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select * from f_buscar_documentos(%s, %s, %s, %s)
    """, (memo, codigo, tipo, subtipo))

    datos = cur.fetchall()

    con.close()
    return datos

def buscar_tramites(
    proveedor=None,
    unidad=None,
    estado=None,
    fecha_desde=None,
    fecha_hasta=None,
    anio=None,
    mes=None
):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select * from f_buscar_tramites(
            %s,%s,%s,%s,%s,%s,%s
        )
    """, (
        proveedor,
        unidad,
        estado,
        fecha_desde,
        fecha_hasta,
        anio,
        mes
    ))

    datos = cur.fetchall()
    con.close()
    return datos
