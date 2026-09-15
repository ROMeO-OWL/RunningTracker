import sqlite3
from typing import List, Optional
from config.settings import DB_PATH
from database.models import RunRecord

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Inicializa la base de datos asegurando que existan todas las columnas necesarias."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Crear la tabla base si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    date TEXT,
                    distance REAL,
                    hours INTEGER,
                    minutes INTEGER,
                    seconds INTEGER,
                    total_seconds INTEGER,
                    pace TEXT,
                    activity_type TEXT,
                    notes TEXT,
                    is_synced INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Migraciones preventivas para bases de datos existentes
            columns_to_add = [
                ("total_seconds", "INTEGER DEFAULT 0"),
                ("is_synced", "INTEGER DEFAULT 0"),
                ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            ]
            
            for column_name, column_type in columns_to_add:
                try:
                    cursor.execute(f"ALTER TABLE runs ADD COLUMN {column_name} {column_type}")
                except sqlite3.OperationalError:
                    pass  # La columna ya existe
                    
            conn.commit()

    def insert_run(self, run: RunRecord) -> bool:
        try:
            # Obtener el estado is_synced del objeto si existe, de lo contrario por defecto 0
            is_synced_val = getattr(run, 'is_synced', getattr(run, 'synced', 0))
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO runs (
                        run_id, date, distance, hours, minutes, seconds,
                        total_seconds, pace, activity_type, notes, is_synced
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    run.run_id, run.date, run.distance, run.hours, run.minutes,
                    run.seconds, run.total_seconds, run.pace, run.activity_type,
                    run.notes, is_synced_val
                ))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error DB Insert: {e}")
            return False

    def get_all_runs(self):
        """Recupera todos los registros ordenados por fecha y los retorna como lista de RunRecord."""
        query = "SELECT * FROM runs ORDER BY date DESC, rowid DESC"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                
                runs = []
                for row in rows:
                    total_sec = row["total_seconds"]
                    if total_sec is None:
                        total_sec = (row["hours"] * 3600) + (row["minutes"] * 60) + row["seconds"]

                    run = RunRecord(
                        run_id=row["run_id"],
                        date=row["date"],
                        distance=row["distance"],
                        hours=row["hours"],
                        minutes=row["minutes"],
                        seconds=row["seconds"],
                        total_seconds=total_sec,
                        pace=row["pace"],
                        activity_type=row["activity_type"],
                        notes=row["notes"]
                    )
                    
                    if hasattr(run, 'is_synced'):
                        run.is_synced = row["is_synced"]
                    elif hasattr(run, 'synced'):
                        run.synced = row["is_synced"]
                    
                    runs.append(run)
                return runs
        except Exception as e:
            print(f"[DB ERROR] Error en get_all_runs: {e}")
            return []

    def get_unsynced_runs(self) -> List[RunRecord]:
        runs = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM runs WHERE is_synced = 0 ORDER BY date ASC')
            rows = cursor.fetchall()
            for r in rows:
                total_sec = r['total_seconds']
                if total_sec is None:
                    total_sec = (r['hours'] * 3600) + (r['minutes'] * 60) + r['seconds']

                run = RunRecord(
                    run_id=r['run_id'],
                    date=r['date'],
                    distance=r['distance'],
                    hours=r['hours'],
                    minutes=r['minutes'],
                    seconds=r['seconds'],
                    total_seconds=total_sec,
                    pace=r['pace'],
                    activity_type=r['activity_type'],
                    notes=r['notes']
                )
                
                if hasattr(run, 'is_synced'):
                    run.is_synced = r['is_synced']
                elif hasattr(run, 'synced'):
                    run.synced = r['is_synced']
                    
                runs.append(run)
        return runs

    def mark_as_synced(self, run_id: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE runs SET is_synced = 1 WHERE run_id = ?', (run_id,))
            conn.commit()
        
    def delete_run(self, run_id: str) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM runs WHERE run_id = ?', (run_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error DB Delete: {e}")
            return False
        
    def get_run_by_id(self, run_id: str):
        """Verifica si un registro ya existe en SQLite local."""
        query = "SELECT * FROM runs WHERE run_id = ?"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (run_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"[DB ERROR] Error en get_run_by_id: {e}")
            return None
        
    def insert_run_direct(self, run_id: str, date: str, distance: float, hours: int, minutes: int, seconds: int, pace: str, activity_type: str, notes: str, is_synced: int = 1):
        """Inserta o actualiza un registro traído de Sheets calculando total_seconds."""
        total_sec = (hours * 3600) + (minutes * 60) + seconds
        
        query = """
            INSERT OR REPLACE INTO runs 
            (run_id, date, distance, hours, minutes, seconds, total_seconds, pace, activity_type, notes, is_synced)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (run_id, date, distance, hours, minutes, seconds, total_sec, pace, activity_type, notes, is_synced))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB ERROR] Error en insert_run_direct: {e}")
            return False