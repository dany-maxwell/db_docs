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
                select * from v_documentos_tramite where tramite_id = %s
                """, (id_tramite,))
    
    dato = cur.fetchone()
    
    con.close()

def busqueda_documentos_por_codigo(texto):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
                select * from v_busqueda_por_codigo = %s
                """, (f"%{texto}%",))
    
    dato = cur.fetchone()
    
    con.close()