"""Helper para ejecutar queries de forma limpia y eficiente"""
from db.connection import get_connection

def ejecutar_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Ejecuta una query de forma segura usando context manager.
    
    Args:
        query: String SQL a ejecutar
        params: Parámetros para la query
        fetch_one: Si True, retorna solo un registro (fetchone)
        fetch_all: Si True, retorna todos los registros (fetchall)
        commit: Si True, hace commit de la transacción
    """
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
