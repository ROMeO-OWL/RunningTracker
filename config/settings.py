import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def get_resource_path(relative_path: str) -> Path:
    """Obtiene la ruta absoluta para recursos, compatible con desarrollo y PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent.parent / relative_path

# Base Path dinámico (Usa la carpeta donde se ejecuta el script/EXE)
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env integradas en el binario o locales
env_path = get_resource_path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Google Sheets Config
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Running")

# Convertimos a string explícito para evitar problemas de compatibilidad con librerías nativas C
CREDENTIALS_PATH = str(get_resource_path("credentials/credentials.json"))
ICON_PATH = str(get_resource_path("ui/assets/app_icon.ico"))

# SQLite Config (Mantiene la DB persistente al lado del archivo .exe)
DB_PATH = BASE_DIR / "data" / "running.db"

# Asegurar que existan los directorios requeridos en el directorio persistente
(BASE_DIR / "data").mkdir(exist_ok=True)

# UI Theme Config (Rojo / Blanco / Negro)
THEME_COLORS = {
    "bg_dark": "#121212",       # Fondo principal oscuro
    "card_bg": "#1E1E1E",       # Tarjetas / contenedores
    "card_border": "#2A2A2A",   # Bordes sutiles
    "primary": "#E50914",       # Rojo de acento (Running Red)
    "primary_hover": "#B80710", # Rojo al pasar el mouse
    "text_white": "#FFFFFF",    # Texto principal
    "text_gray": "#A0A0A0",     # Texto secundario
    "success": "#2E7D32",      # Sincronizado (Verde)
    "pending": "#F57C00",      # Pendiente (Naranja)
    "error": "#D32F2F"         # Error (Rojo suave)
}