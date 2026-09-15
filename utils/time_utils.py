import uuid
from datetime import datetime

def calculate_pace(distance_km: float, total_seconds: int) -> str:
    """
    Calcula el ritmo promedio en formato MM:SS /km de forma exacta.
    """
    if distance_km <= 0 or total_seconds <= 0:
        return "00:00"

    # Segundos por kilometro
    sec_per_km = total_seconds / distance_km
    pace_minutes = int(sec_per_km // 60)
    pace_seconds = int(round(sec_per_km % 60))

    if pace_seconds == 60:
        pace_minutes += 1
        pace_seconds = 0

    return f"{pace_minutes:02d}:{pace_seconds:02d}"

def generate_unique_run_id(date_str: str) -> str:
    """
    Genera un ID único para el registro (ej: RUN-20260910-A1B2)
    """
    clean_date = date_str.replace("-", "")
    short_uuid = uuid.uuid4().hex[:4].upper()
    return f"RUN-{clean_date}-{short_uuid}"

def format_seconds_to_time(total_seconds: int) -> str:
    """
    Convierte segundos a HH:MM:SS
    """
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
