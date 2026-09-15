import threading
import customtkinter as ctk
from datetime import datetime
from config.settings import THEME_COLORS
from utils.validators import validate_run_input
from utils.time_utils import calculate_pace, generate_unique_run_id
from database.models import RunRecord

class RegisterView(ctk.CTkFrame):
    def __init__(self, parent, db, sync_service, on_success_callback):
        super().__init__(parent, fg_color=THEME_COLORS["bg_dark"])
        self.db = db
        self.sync_service = sync_service
        self.on_success_callback = on_success_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(
            self, 
            text="NUEVO REGISTRO DE RUNNING", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=THEME_COLORS["text_white"]
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="w")

        # 1. Distancia
        lbl_dist = ctk.CTkLabel(self, text="Distancia (km):", font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME_COLORS["text_white"])
        lbl_dist.grid(row=1, column=0, sticky="w", pady=(5, 2))
        
        self.entry_dist = ctk.CTkEntry(self, placeholder_text="Ej: 5.0, 7.5, 10.0", fg_color=THEME_COLORS["card_bg"])
        self.entry_dist.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # 2. Tiempo (Horas, Min, Seg)
        lbl_time = ctk.CTkLabel(self, text="Tiempo Transcurrido:", font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME_COLORS["text_white"])
        lbl_time.grid(row=3, column=0, sticky="w", pady=(5, 2))

        time_frame = ctk.CTkFrame(self, fg_color="transparent")
        time_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        time_frame.grid_columnconfigure((0,1,2), weight=1)

        self.entry_hrs = ctk.CTkEntry(time_frame, placeholder_text="Horas (00)", fg_color=THEME_COLORS["card_bg"])
        self.entry_hrs.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.entry_min = ctk.CTkEntry(time_frame, placeholder_text="Minutos (0-59)", fg_color=THEME_COLORS["card_bg"])
        self.entry_min.grid(row=0, column=1, padx=5, sticky="ew")

        self.entry_sec = ctk.CTkEntry(time_frame, placeholder_text="Segundos (0-59)", fg_color=THEME_COLORS["card_bg"])
        self.entry_sec.grid(row=0, column=2, padx=(5, 0), sticky="ew")

        # 3. Tipo de actividad
        lbl_type = ctk.CTkLabel(self, text="Tipo de Actividad:", font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME_COLORS["text_white"])
        lbl_type.grid(row=5, column=0, sticky="w", pady=(5, 2))

        activity_options = ["Entrenamiento", "Carrera", "Competencia", "Trail", "Tempo", "Intervalos", "Fondo", "Recuperación", "Otro"]
        self.combo_type = ctk.CTkOptionMenu(self, values=activity_options, fg_color=THEME_COLORS["card_bg"], button_color=THEME_COLORS["primary"])
        self.combo_type.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # 4. Fecha
        lbl_date = ctk.CTkLabel(self, text="Fecha (YYYY-MM-DD):", font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME_COLORS["text_white"])
        lbl_date.grid(row=7, column=0, sticky="w", pady=(5, 2))

        self.entry_date = ctk.CTkEntry(self, fg_color=THEME_COLORS["card_bg"])
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # 5. Observaciones
        lbl_notes = ctk.CTkLabel(self, text="Observaciones (Opcional):", font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME_COLORS["text_white"])
        lbl_notes.grid(row=9, column=0, sticky="w", pady=(5, 2))

        self.entry_notes = ctk.CTkEntry(self, placeholder_text="Ej: Sensación de cansancio, buen clima...", fg_color=THEME_COLORS["card_bg"])
        self.entry_notes.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Mensaje de estado / error
        self.lbl_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11))
        self.lbl_status.grid(row=11, column=0, columnspan=2, pady=(0, 10))

        # Botón Guardar
        btn_save = ctk.CTkButton(
            self,
            text="GUARDAR ENTRENAMIENTO",
            fg_color=THEME_COLORS["primary"],
            hover_color=THEME_COLORS["primary_hover"],
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            command=self.save_record
        )
        btn_save.grid(row=12, column=0, columnspan=2, sticky="ew", pady=5)

    def save_record(self):
        self.lbl_status.configure(text="")

        dist_str = self.entry_dist.get()
        hrs_str = self.entry_hrs.get()
        min_str = self.entry_min.get()
        sec_str = self.entry_sec.get()
        date_str = self.entry_date.get()
        act_type = self.combo_type.get()
        notes = self.entry_notes.get()

        is_valid, err_msg, parsed = validate_run_input(dist_str, hrs_str, min_str, sec_str, date_str, act_type)
        if not is_valid:
            self.lbl_status.configure(text=f"❌ {err_msg}", text_color=THEME_COLORS["error"])
            return

        pace = calculate_pace(parsed["distance"], parsed["total_seconds"])
        run_id = generate_unique_run_id(parsed["date"])

        new_run = RunRecord(
            run_id=run_id,
            date=parsed["date"],
            distance=parsed["distance"],
            hours=parsed["hours"],
            minutes=parsed["minutes"],
            seconds=parsed["seconds"],
            total_seconds=parsed["total_seconds"],
            pace=pace,
            activity_type=parsed["activity_type"],
            notes=notes,
            synced=0
        )

        # 1. Guardar localmente
        db_saved = self.db.insert_run(new_run)
        if not db_saved:
            self.lbl_status.configure(text="❌ Error al guardar en base de datos local.", text_color=THEME_COLORS["error"])
            return

        # 2. Sincronizar en segundo plano sin congelar la app
        threading.Thread(target=self._async_sync, daemon=True).start()

        self.lbl_status.configure(text="✓ Guardado localmente. Sincronizando...", text_color=THEME_COLORS["success"])
        
        self.entry_dist.delete(0, 'end')
        self.entry_hrs.delete(0, 'end')
        self.entry_min.delete(0, 'end')
        self.entry_sec.delete(0, 'end')
        self.entry_notes.delete(0, 'end')

        if self.on_success_callback:
            self.after(1000, self.on_success_callback)

    def _async_sync(self):
        success, fail, msg = self.sync_service.sync_pending_records()
        print(f"[SYNC]: {msg}")