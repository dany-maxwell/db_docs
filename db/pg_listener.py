from db.connection import get_connection
import os, time
import psycopg2
from dotenv import load_dotenv
import threading
import select
from PySide6.QtCore import QObject, Signal


class PgNotifyListener(QObject):
    notify_received = Signal(str)

    def __init__(self, channel):
           super().__init__()
           self.channel = channel  
           self._stop_event = threading.Event()
           self._thread = threading.Thread(target=self._listen, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()

    def _listen(self):
        while not self._stop_event.is_set():
            conn = None
            try:
                conn = psycopg2.connect(
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT")
                )
                conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()
                cur.execute(f"LISTEN {self.channel};")

                while not self._stop_event.is_set():
                    if select.select([conn], [], [], 1) == ([], [], []):
                        continue

                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        self.notify_received.emit(notify.payload)
            except (psycopg2.OperationalError, Exception) as e:
                time.sleep(5)
            finally:
                if conn:
                    cur.close()
                    conn.close()