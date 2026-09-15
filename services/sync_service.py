from database.database import DatabaseManager
from services.google_sheets import GoogleSheetsService
from database.models import RunRecord

class SyncService:
    def __init__(self, db: DatabaseManager, sheets_service: GoogleSheetsService):
        self.db = db
        self.sheets_service = sheets_service

    def sync_pending_records(self) -> tuple[int, int, str]:
        """
        Sincroniza todos los registros pendientes en SQLite hacia Google Sheets.
        Retorna (exitosos, fallidos, mensaje).
        """
        unsynced = self.db.get_unsynced_runs()
        if not unsynced:
            return 0, 0, "No hay registros pendientes por sincronizar."

        connected, msg = self.sheets_service.connect()
        if not connected:
            return 0, len(unsynced), f"Sin conexión a Google Sheets: {msg}"

        success_count = 0
        fail_count = 0

        for run in unsynced:
            ok, err_msg = self.sheets_service.append_run(run)
            if ok:
                self.db.mark_as_synced(run.run_id)
                success_count += 1
            else:
                fail_count += 1

        return success_count, fail_count, f"Sincronizados {success_count}/{len(unsynced)} registros."

    def pull_from_sheets_to_sqlite(self) -> tuple[int, str]:
        connected, msg = self.sheets_service.connect()
        if not connected:
            return 0, f"Sin conexión a Google Sheets: {msg}"

        records = self.sheets_service.fetch_all_records()
        if not records:
            return 0, "Sin registros o error al obtener datos."

        imported_count = 0
        for row in records:
            try:
                r = {str(k).strip(): v for k, v in row.items()}
                
                run_id = str(r.get("ID", "")).strip()
                if not run_id:
                    continue

                if self.db.get_run_by_id(run_id):
                    continue

                date_val = str(r.get("Fecha", ""))
                dist_val = float(r.get("Distancia (km)", 0))
                
                time_str = str(r.get("Tiempo Total", "00:00:00")).strip()
                time_parts = time_str.split(":")
                
                if len(time_parts) == 3:
                    h, m, s = map(int, time_parts)
                elif len(time_parts) == 2:
                    h = 0
                    m, s = map(int, time_parts)
                else:
                    h, m, s = 0, 0, 0

                pace_val = str(r.get("Ritmo (min/km)", ""))
                type_val = str(r.get("Tipo", "Entrenamiento"))
                notes_val = str(r.get("Observaciones", ""))

                self.db.insert_run_direct(
                    run_id=run_id,
                    date=date_val,
                    distance=dist_val,
                    hours=h,
                    minutes=m,
                    seconds=s,
                    pace=pace_val,
                    activity_type=type_val,
                    notes=notes_val,
                    is_synced=1
                )
                imported_count += 1
            except Exception as e:
                print(f"[PULL ROW ERROR] Fila omitida: {row} -> Error: {e}")
                continue

        return imported_count, f"Importados: {imported_count}"