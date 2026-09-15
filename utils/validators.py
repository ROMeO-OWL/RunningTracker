from datetime import datetime
from typing import Tuple, Optional

def validate_run_input(
    distance_str: str,
    hours_str: str,
    minutes_str: str,
    seconds_str: str,
    date_str: str,
    activity_type: str
) -> Tuple[bool, Optional[str], dict]:
    """
    Valida exhaustivamente todos los campos del formulario.
    """
    # 1. Distancia
    try:
        distance = float(distance_str.replace(',', '.'))
        if distance <= 0:
            return False, "La distancia debe ser un número mayor a 0.", {}
        if distance > 300:
            return False, "Distancia excesiva. Ingresa un valor menor a 300 km.", {}
    except ValueError:
        return False, "Ingresa un valor numérico válido para la distancia.", {}

    # 2. Horas
    try:
        hours = int(hours_str) if hours_str.strip() else 0
        if hours < 0 or hours > 24:
            return False, "Las horas deben estar entre 0 y 24.", {}
    except ValueError:
        return False, "Las horas deben ser un número entero.", {}

    # 3. Minutos
    try:
        minutes = int(minutes_str) if minutes_str.strip() else 0
        if minutes < 0 or minutes > 59:
            return False, "Los minutos deben estar entre 0 y 59.", {}
    except ValueError:
        return False, "Los minutos deben ser un número entero.", {}

    # 4. Segundos
    try:
        seconds = int(seconds_str) if seconds_str.strip() else 0
        if seconds < 0 or seconds > 59:
            return False, "Los segundos deben estar entre 0 y 59.", {}
    except ValueError:
        return False, "Los segundos deben ser un número entero.", {}

    # Validar tiempo total mayor a 0
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    if total_seconds <= 0:
        return False, "El tiempo total debe ser mayor a 0 segundos.", {}

    # 5. Fecha
    try:
        valid_date = datetime.strptime(date_str, "%Y-%m-%d")
        if valid_date.year < 2000 or valid_date.year > 2100:
            return False, "Ingresa un año razonable.", {}
    except ValueError:
        return False, "La fecha debe tener el formato YYYY-MM-DD.", {}

    # 6. Tipo de actividad
    if not activity_type or activity_type.strip() == "":
        return False, "Debes seleccionar un tipo de actividad.", {}

    parsed_data = {
        "distance": round(distance, 2),
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "total_seconds": total_seconds,
        "date": date_str,
        "activity_type": activity_type.strip()
    }
    return True, None, parsed_data
