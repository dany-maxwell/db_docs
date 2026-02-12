import psycopg2
from psycopg2 import pool
import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

_connection_pool = None

def _get_pool():
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = pool.SimpleConnectionPool(
            1, 5,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
    return _connection_pool

@contextmanager
def get_connection():
    conn = _get_pool().getconn()
    try:
        yield conn
    finally:
        _get_pool().putconn(conn)

# Para casos donde se necesita una conexión persistente (ej: listener)
def get_raw_connection():
    return _get_pool().getconn()