from dataclasses import dataclass
from typing import Optional

@dataclass
class RunRecord:
    run_id: str
    date: str              # YYYY-MM-DD
    distance: float        # km
    hours: int
    minutes: int
    seconds: int
    total_seconds: int
    pace: str              # mm:ss /km
    activity_type: str
    notes: Optional[str] = ""
    synced: int = 0        # 0: No sincronizado, 1: Sincronizado
    created_at: Optional[str] = None

    def to_dict(self):
        return {
            "ID": self.run_id,
            "Fecha": self.date,
            "Distancia (km)": f"{self.distance:.2f}",
            "Tiempo Total": f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}",
            "Ritmo (min/km)": self.pace,
            "Tipo": self.activity_type,
            "Observaciones": self.notes or ""
        }
