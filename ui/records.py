import customtkinter as ctk
from config.settings import THEME_COLORS
from services.statistics import StatisticsService

class RecordsView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, fg_color=THEME_COLORS["bg_dark"])
        self.db = db

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(
            self, 
            text="🏆 RÉCORDS PERSONALES", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=THEME_COLORS["text_white"]
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="w")

        runs = self.db.get_all_runs()
        records = StatisticsService.get_personal_records(runs)

        dist_keys = ["5.0K", "10.0K", "21.1K", "42.2K"]
        row_idx = 1
        col_idx = 0

        for key in dist_keys:
            run = records.get(key)
            card = ctk.CTkFrame(self, fg_color=THEME_COLORS["card_bg"], corner_radius=10, border_width=1, border_color=THEME_COLORS["card_border"])
            card.grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="nsew")

            lbl_dist = ctk.CTkLabel(card, text=f"MEJOR {key}", font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME_COLORS["primary"])
            lbl_dist.pack(anchor="w", padx=15, pady=(12, 2))

            if run:
                time_str = f"{run.hours:02d}:{run.minutes:02d}:{run.seconds:02d}"
                lbl_time = ctk.CTkLabel(card, text=time_str, font=ctk.CTkFont(size=20, weight="bold"), text_color=THEME_COLORS["text_white"])
                lbl_time.pack(anchor="w", padx=15, pady=2)

                details = f"⚡ {run.pace}/km   📅 {run.date}"
                lbl_det = ctk.CTkLabel(card, text=details, font=ctk.CTkFont(size=10), text_color=THEME_COLORS["text_gray"])
                lbl_det.pack(anchor="w", padx=15, pady=(2, 12))
            else:
                lbl_none = ctk.CTkLabel(card, text="Sin registros", font=ctk.CTkFont(size=14), text_color=THEME_COLORS["text_gray"])
                lbl_none.pack(anchor="w", padx=15, pady=(5, 15))

            col_idx += 1
            if col_idx > 1:
                col_idx = 0
                row_idx += 1
