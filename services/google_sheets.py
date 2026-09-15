import os
import gspread
from google.oauth2.service_account import Credentials
from config.settings import CREDENTIALS_PATH, GOOGLE_SHEET_ID, GOOGLE_SHEET_NAME
from database.models import RunRecord

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class GoogleSheetsService:
    def __init__(self):
        self.client = None
        self.sheet = None

    def connect(self) -> tuple[bool, str]:
        if not os.path.exists(CREDENTIALS_PATH):
            print(f"[ERROR] Ruta no encontrada: {CREDENTIALS_PATH}")
            return False, "credentials.json no encontrado"

        try:
            creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
            self.client = gspread.authorize(creds)
            self.client.http_client.timeout = 10
            
            spreadsheet = self.client.open_by_key(GOOGLE_SHEET_ID)
            self.sheet = spreadsheet.worksheet(GOOGLE_SHEET_NAME)
            return True, "Conectado"
        except Exception as e:
            # IMPRIMIR DETALLE EN CONSOLA
            print(f"\n================ ERROR DE CONEXIÓN ================")
            print(f"Tipo: {type(e).__name__}")
            print(f"Detalle: {str(e)}")
            print(f"==================================================\n")
            return False, str(e)
    def append_run(self, run: RunRecord) -> tuple[bool, str]:
        if not self.sheet:
            connected, msg = self.connect()
            if not connected:
                return False, msg

        try:
            row = [
                run.run_id,
                run.date,
                run.distance,
                f"{run.hours:02d}:{run.minutes:02d}:{run.seconds:02d}",
                run.pace,
                run.activity_type,
                run.notes or ""
            ]
            self.sheet.append_row(row)
            return True, "Registro guardado en Google Sheets"
        except Exception as e:
            return False, f"Error al insertar en Google Sheets: {str(e)}"

    def delete_run(self, run_id: str) -> tuple[bool, str]:
        if not self.sheet:
            connected, msg = self.connect()
            if not connected:
                return False, msg

        try:
            cell = self.sheet.find(run_id)
            if cell:
                self.sheet.delete_rows(cell.row)
                return True, "Registro eliminado de Google Sheets"
            return False, "Registro no encontrado en Google Sheets"
        except Exception as e:
            return False, f"Error al eliminar en Google Sheets: {str(e)}"

    def fetch_all_records(self) -> list[dict]:
        if not self.sheet:
            connected, _ = self.connect()
            if not connected:
                return []

        try:
            records = self.sheet.get_all_records()
            return records
        except Exception as e:
            print(f"[SHEETS FETCH ERROR]: {e}")
            return []