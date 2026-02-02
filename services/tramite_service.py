from db.connection import get_connection


def crear_tramite(proveedor_id, unidad_id, estado):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        insert into tramite
        (proveedor_id, unidad_id, estado, fecha_creacion)
        values (%s, %s, %s, now())
        returning id
    """, (proveedor_id, unidad_id, estado))

    id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return id
