from db.connection import get_connection


def crear_documento_con_numeracion(
    tramite_id,
    tipo_documento_id,
    subtipo_documento_id,
    codigo_manual,
    unidad_codigo,
    documento_origen_id=None
):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        select crear_documento(
            %s, %s, %s, %s, %s, %s
        )
    """, (
        tramite_id,
        tipo_documento_id,
        subtipo_documento_id,
        documento_origen_id,
        codigo_manual,
        unidad_codigo
    ))

    id_doc = cur.fetchone()[0]

    cur.execute("""
        select codigo_final, fecha_documento
        from documento
        where id = %s
    """, (id_doc,))

    codigo_generado, fecha = cur.fetchone()

    con.commit()
    cur.close()
    con.close()

    return {
        "id": id_doc,
        "codigo": codigo_generado,
        "fecha": fecha
}