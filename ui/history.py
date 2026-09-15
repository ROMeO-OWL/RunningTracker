import threading
import customtkinter as ctk
from config.settings import THEME_COLORS

class HistoryView(ctk.CTkFrame):
    def __init__(self, parent, db, sheets_service):
        super().__init__(parent, fg_color=THEME_COLORS["bg_dark"])
        self.db = db
        self.sheets_service = sheets_service

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(
            self, 
            text="HISTORIAL DE ENTRENAMIENTOS", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=THEME_COLORS["text_white"]
        )
        title.grid(row=0, column=0, pady=(10, 15), sticky="w")

        # Filtros
        filter_frame = ctk.CTkFrame(self, fg_color=THEME_COLORS["card_bg"])
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        filter_frame.grid_columnconfigure(0, weight=1)

        self.entry_search = ctk.CTkEntry(filter_frame, placeholder_text="Buscar por observación o tipo...", fg_color=THEME_COLORS["bg_dark"])
        self.entry_search.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_search = ctk.CTkButton(
            filter_frame, 
            text="Filtrar", 
            fg_color=THEME_COLORS["primary"],
            hover_color=THEME_COLORS["primary_hover"],
            width=80,
            command=self.load_history
        )
        btn_search.grid(row=0, column=1, padx=10, pady=10)

        # Scrollable Frame para la tabla/lista
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=THEME_COLORS["card_bg"], corner_radius=10)
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.load_history()

    def load_history(self):
        # Limpiar lista previa
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        runs = self.db.get_all_runs()
        search_query = self.entry_search.get().lower().strip()

        if search_query:
            runs = [r for r in runs if search_query in r.activity_type.lower() or search_query in (r.notes or "").lower()]

        if not runs:
            lbl = ctk.CTkLabel(self.scroll_frame, text="No se encontraron registros.", text_color=THEME_COLORS["text_gray"])
            lbl.pack(pady=20)
            return

        for r in runs:
            sync_icon = "🟢" if r.synced == 1 else "🟡"
            card = ctk.CTkFrame(self.scroll_frame, fg_color=THEME_COLORS["bg_dark"], corner_radius=6)
            card.pack(fill="x", padx=5, pady=4)

            # Usar grid interno para separar información del botón eliminar
            card.grid_columnconfigure(0, weight=1)

            text_container = ctk.CTkFrame(card, fg_color="transparent")
            text_container.grid(row=0, column=0, sticky="w", padx=10, pady=6)

            main_text = f"{sync_icon} {r.date}  |  {r.distance:.2f} km  |  Tiempo: {r.hours:02d}:{r.minutes:02d}:{r.seconds:02d}  |  Ritmo: {r.pace}/km"
            sub_text = f"Tipo: {r.activity_type}"
            if r.notes:
                sub_text += f"  |  Obs: {r.notes}"

            lbl_main = ctk.CTkLabel(text_container, text=main_text, font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME_COLORS["text_white"])
            lbl_main.pack(anchor="w")

            lbl_sub = ctk.CTkLabel(text_container, text=sub_text, font=ctk.CTkFont(size=10), text_color=THEME_COLORS["text_gray"])
            lbl_sub.pack(anchor="w")

            # Botón Borrar
            btn_delete = ctk.CTkButton(
                card,
                text="🗑️",
                width=35,
                height=30,
                fg_color="transparent",
                hover_color=THEME_COLORS["error"],
                command=lambda run_id=r.run_id: self.delete_record(run_id)
            )
            btn_delete.grid(row=0, column=1, padx=10, pady=6, sticky="e")

    def delete_record(self, run_id: str):
        # 1. Eliminar de SQLite inmediatamente
        if self.db.delete_run(run_id):
            # 2. Eliminar de Google Sheets en segundo plano
            threading.Thread(
                target=self._async_delete_from_sheets, 
                args=(run_id,), 
                daemon=True
            ).start()
            
            # 3. Recargar la lista en pantalla
            self.load_history()

    def _async_delete_from_sheets(self, run_id: str):
        ok, msg = self.sheets_service.delete_run(run_id)
        print(f"[SHEETS DELETE]: {msg}")