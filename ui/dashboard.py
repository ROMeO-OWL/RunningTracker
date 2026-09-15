import customtkinter as ctk
from config.settings import THEME_COLORS
from services.statistics import StatisticsService

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, db, navigate_to_register_cb):
        super().__init__(parent, fg_color=THEME_COLORS["bg_dark"])
        self.db = db
        self.navigate_to_register_cb = navigate_to_register_cb

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.build_ui()

    def build_ui(self):
        # Título
        title = ctk.CTkLabel(
            self, 
            text="DASHBOARD DE RUNNING", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME_COLORS["text_white"]
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="w")

        # Cargar datos
        runs = self.db.get_all_runs()
        stats = StatisticsService.get_summary_stats(runs)

        # Tarjeta 1: Entrenamientos Totales
        self.create_card(0, 1, 0, "ENTRENAMIENTOS", str(stats["total_runs"]), "sesiones registradas")
        # Tarjeta 2: Kilómetros Totales
        self.create_card(0, 1, 1, "KM TOTALES", f"{stats['total_kms']} km", "distancia acumulada")
        # Tarjeta 3: Mejor Ritmo
        self.create_card(1, 2, 0, "MEJOR RITMO", stats["best_pace"], "máximo rendimiento")
        # Tarjeta 4: Carrera más Larga
        self.create_card(1, 2, 1, "MAYOR DISTANCIA", f"{stats['longest_run']} km", "distancia máxima")

        # Sección Recientes
        recent_title = ctk.CTkLabel(
            self, 
            text="ÚLTIMOS ENTRENAMIENTOS", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME_COLORS["primary"]
        )
        recent_title.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="w")

        # Contenedor de lista reciente
        list_frame = ctk.CTkFrame(self, fg_color=THEME_COLORS["card_bg"], corner_radius=10)
        list_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=5)
        list_frame.grid_columnconfigure(0, weight=1)

        recent_runs = runs[:3] if runs else []
        if not recent_runs:
            lbl = ctk.CTkLabel(list_frame, text="No hay entrenamientos registrados aún.", text_color=THEME_COLORS["text_gray"])
            lbl.pack(pady=20)
        else:
            for r in recent_runs:
                item_str = f"📅 {r.date}   |   🏃 {r.distance} km   |   ⏱️ {r.hours:02d}:{r.minutes:02d}:{r.seconds:02d}   |   ⚡ {r.pace}/km   |   📌 {r.activity_type}"
                lbl = ctk.CTkLabel(list_frame, text=item_str, text_color=THEME_COLORS["text_white"], font=ctk.CTkFont(size=12))
                lbl.pack(anchor="w", padx=15, pady=8)

        # Botón Acción Rápida
        btn_new = ctk.CTkButton(
            self,
            text="+ REGISTRAR NUEVO TIEMPO",
            fg_color=THEME_COLORS["primary"],
            hover_color=THEME_COLORS["primary_hover"],
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            command=self.navigate_to_register_cb
        )
        btn_new.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew")

    def create_card(self, row, grid_row, grid_col, title_text, val_text, sub_text):
        card = ctk.CTkFrame(self, fg_color=THEME_COLORS["card_bg"], corner_radius=10, border_width=1, border_color=THEME_COLORS["card_border"])
        card.grid(row=grid_row, column=grid_col, padx=8, pady=8, sticky="nsew")
        
        lbl_title = ctk.CTkLabel(card, text=title_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=THEME_COLORS["text_gray"])
        lbl_title.pack(anchor="w", padx=15, pady=(12, 2))

        lbl_val = ctk.CTkLabel(card, text=val_text, font=ctk.CTkFont(size=22, weight="bold"), text_color=THEME_COLORS["primary"])
        lbl_val.pack(anchor="w", padx=15, pady=2)

        lbl_sub = ctk.CTkLabel(card, text=sub_text, font=ctk.CTkFont(size=10), text_color=THEME_COLORS["text_gray"])
        lbl_sub.pack(anchor="w", padx=15, pady=(2, 12))
