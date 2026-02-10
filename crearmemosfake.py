from db.connection import get_connection

def generar_memos_fake(n=1000):
    conn = get_connection()
    cur = conn.cursor()

    for i in range(1, n+1):

        memo = f"MEMO-2025-{str(i).zfill(4)}"

        # Crear trámite
        cur.execute("""
            INSERT INTO tramite (proveedor_id, unidad_id, estado)
            VALUES (1, 1, 'EN INSTRUCCION')
            RETURNING id
        """)

        tramite_id = cur.fetchone()[0]

        # Crear memo
        cur.execute("""
            INSERT INTO documento (
                tramite_id,
                tipo_documento_id,
                codigo_final,
                es_manual
            )
            VALUES (%s, 1, %s, true)
        """, (tramite_id, memo))

    conn.commit()
    print(f" Creados {n} trámites con memos fake")

generar_memos_fake()
