from db.connection import get_connection

def busqueda_proveedor_por_memo(id_memo):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
                select p.id, p.nombre from proveedor p 
                join tramite t on p.id = t.proveedor_id
                join documento d on t.id = d.tramite_id
                where d.id = %s;                
                """, (id_memo,))

    dato = cur.fetchone()
    con.close()

    return dato

def busqueda_tramite_por_memo(id_memo):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
                select t.id from tramite t
                join documento d on t.id = d.tramite_id
                where d.id = %s;                
                """, (id_memo,))

    dato = cur.fetchone()
    con.close()

    return dato