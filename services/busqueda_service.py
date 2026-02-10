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

def busqueda_documentos_avanzada(
    memo=None,
    proveedor=None,
    unidad=None,
    tipo=None,
    subtipo=None,
    estado=None,
    codigo=None,
    fecha_desde=None,
    fecha_hasta=None
):
    con = get_connection()
    cur = con.cursor()

    query = "select * from v_busqueda_avanzada where 1=1"
    params = []

    if memo:
        query += " and memo_id = %s"
        params.append(memo)

    if proveedor:
        query += " and proveedor_id = %s"
        params.append(proveedor)

    if unidad:
        query += " and unidad_id = %s"
        params.append(unidad)

    if tipo:
        query += " and tipo_id = %s"
        params.append(tipo)

    if subtipo:
        query += " and subtipo_id = %s"
        params.append(subtipo)

    if estado:
        query += " and estado = %s"
        params.append(estado)

    if codigo:
        query += " and codigo ilike %s"
        params.append(f"%{codigo}%")

    if fecha_desde:
        query += " and fecha >= %s"
        params.append(fecha_desde)

    if fecha_hasta:
        query += " and fecha <= %s"
        params.append(fecha_hasta)

    query += " order by documento_id desc"

    cur.execute(query, params)
    datos = cur.fetchall()

    con.close()
    return datos
