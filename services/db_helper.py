from db.connection import get_connection
from psycopg2.extras import RealDictCursor

def ejecutar_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            
            if commit:
                conn.commit()
                return cur.fetchone() if fetch_one else None
            
            if fetch_one:
                result = cur.fetchone()
                return dict(result) if result else None
            elif fetch_all:
                return [dict(row) for row in cur.fetchall()]
            else:
                return None
