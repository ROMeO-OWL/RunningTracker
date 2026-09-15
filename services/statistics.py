from typing import List, Dict, Optional, Any
from database.models import RunRecord
from utils.time_utils import calculate_pace, format_seconds_to_time

class StatisticsService:
    @staticmethod
    def _get_val(obj: Any, attr: str, default: Any = 0) -> Any:
        """Extrae un valor de forma segura, ya sea atributo u clave de diccionario/Row."""
        if hasattr(obj, attr):
            return getattr(obj, attr)
        elif isinstance(obj, dict) or hasattr(obj, '__getitem__'):
            try:
                return obj[attr]
            except (KeyError, IndexError):
                return default
        return default

    @staticmethod
    def get_summary_stats(runs: List[Any]) -> Dict:
        if not runs:
            return {
                "total_kms": 0.0,
                "total_runs": 0,
                "total_time_str": "0h 0m",
                "best_pace": "--:--",
                "longest_run": 0.0
            }

        # Extracción flexible de propiedades
        total_kms = sum(float(StatisticsService._get_val(r, 'distance', 0)) for r in runs)
        total_runs = len(runs)
        
        # Calcular total_seconds dinámicamente si no está presente en la fila
        def get_seconds(r):
            sec = StatisticsService._get_val(r, 'total_seconds', None)
            if sec is not None:
                return int(sec)
            h = int(StatisticsService._get_val(r, 'hours', 0))
            m = int(StatisticsService._get_val(r, 'minutes', 0))
            s = int(StatisticsService._get_val(r, 'seconds', 0))
            return (h * 3600) + (m * 60) + s

        total_seconds = sum(get_seconds(r) for r in runs)
        
        # Calcular horas y minutos
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        total_time_str = f"{h}h {m}m"

        # Mejor ritmo (menor segundos por km con distancia > 0)
        valid_pace_runs = [
            (get_seconds(r) / float(StatisticsService._get_val(r, 'distance', 0)))
            for r in runs if float(StatisticsService._get_val(r, 'distance', 0)) > 0
        ]

        if valid_pace_runs:
            best_pace_sec = min(valid_pace_runs)
            p_m = int(best_pace_sec // 60)
            p_s = int(round(best_pace_sec % 60))
            best_pace = f"{p_m:02d}:{p_s:02d}"
        else:
            best_pace = "--:--"

        longest_run = max(float(StatisticsService._get_val(r, 'distance', 0)) for r in runs)

        return {
            "total_kms": round(total_kms, 2),
            "total_runs": total_runs,
            "total_time_str": total_time_str,
            "best_pace": f"{best_pace} /km" if best_pace != "--:--" else "--:--",
            "longest_run": round(longest_run, 2)
        }

    @staticmethod
    def get_personal_records(runs: List[Any]) -> Dict[str, Optional[Any]]:
        """Detecta mejores tiempos para distancias clave y agrupa las demás."""
        targets = [5.0, 10.0, 21.1, 42.2]
        records = {}

        def get_seconds(r):
            sec = StatisticsService._get_val(r, 'total_seconds', None)
            if sec is not None:
                return int(sec)
            h = int(StatisticsService._get_val(r, 'hours', 0))
            m = int(StatisticsService._get_val(r, 'minutes', 0))
            s = int(StatisticsService._get_val(r, 'seconds', 0))
            return (h * 3600) + (m * 60) + s

        for target in targets:
            # Tolerancia de +/- 0.15 km
            matching_runs = [
                r for r in runs 
                if abs(float(StatisticsService._get_val(r, 'distance', 0)) - target) <= 0.15
            ]
            if matching_runs:
                best_run = min(matching_runs, key=get_seconds)
                records[f"{target}K"] = best_run
            else:
                records[f"{target}K"] = None

        return records