from db.connection import get_connection

def ejecutar_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            
            if commit:
                conn.commit()
                return cur.fetchone() if fetch_one else None
            
            if fetch_one:
                return cur.fetchone()
            elif fetch_all:
                return cur.fetchall()
            else:
                return None
