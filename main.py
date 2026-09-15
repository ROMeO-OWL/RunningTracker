import customtkinter as ctk
import threading
from database.database import DatabaseManager
from services.google_sheets import GoogleSheetsService
from services.sync_service import SyncService
from ui.dashboard import DashboardView
from ui.register import RegisterView
from ui.history import HistoryView
from ui.records import RecordsView
from config.settings import THEME_COLORS, ICON_PATH

class RunningTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de ventana e icono
        self.iconbitmap(str(ICON_PATH))
        self.title("Running Tracker - Gestión Personal")
        
        # Tamaño responsivo ~65% ancho y 70% alto
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 0.65)
        height = int(screen_height * 0.70)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(800, 550)

        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=THEME_COLORS["bg_dark"])

        # Servicios y DB
        self.db = DatabaseManager()
        self.sheets_service = GoogleSheetsService()
        self.sync_service = SyncService(self.db, self.sheets_service)

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Navegación
        self.build_sidebar()

        # Contenedor de Vistas
        self.main_container = ctk.CTkFrame(self, fg_color=THEME_COLORS["bg_dark"])
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Cargar vista por defecto
        self.current_view = None
        self.show_dashboard()

        # Sincronización en segundo plano al iniciar
        threading.Thread(target=self.auto_sync, daemon=True).start()

    def build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=THEME_COLORS["card_bg"], width=180, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(5, weight=1)

        # Logo / Título App
        lbl_logo = ctk.CTkLabel(
            sidebar, 
            text='''🏃 RUNNING\nTRACKER''', 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=THEME_COLORS["primary"]
        )
        lbl_logo.grid(row=0, column=0, padx=15, pady=(20, 25))

        # Botones de navegación
        btn_dash = ctk.CTkButton(
            sidebar, text="Dashboard", fg_color="transparent", 
            text_color=THEME_COLORS["text_white"], anchor="w",
            hover_color=THEME_COLORS["card_border"], command=self.show_dashboard
        )
        btn_dash.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        btn_reg = ctk.CTkButton(
            sidebar, text="+ Registrar", fg_color="transparent", 
            text_color=THEME_COLORS["text_white"], anchor="w",
            hover_color=THEME_COLORS["card_border"], command=self.show_register
        )
        btn_reg.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        btn_hist = ctk.CTkButton(
            sidebar, text="Historial", fg_color="transparent", 
            text_color=THEME_COLORS["text_white"], anchor="w",
            hover_color=THEME_COLORS["card_border"], command=self.show_history
        )
        btn_hist.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        btn_rec = ctk.CTkButton(
            sidebar, text="Récords", fg_color="transparent", 
            text_color=THEME_COLORS["text_white"], anchor="w",
            hover_color=THEME_COLORS["card_border"], command=self.show_records
        )
        btn_rec.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Indicador de estado de Sincronización
        self.lbl_sync_status = ctk.CTkLabel(
            sidebar, text="🟡 Verificando...", font=ctk.CTkFont(size=10), text_color=THEME_COLORS["text_gray"]
        )
        self.lbl_sync_status.grid(row=6, column=0, padx=10, pady=15)

    def trigger_manual_sync(self):
        self.lbl_sync_status.configure(text="⏳ Sincronizando...", text_color=THEME_COLORS["text_gray"])
        threading.Thread(target=self.auto_sync, daemon=True).start()

    def clear_main_container(self):
        if self.current_view:
            self.current_view.destroy()

    def show_dashboard(self):
        self.clear_main_container()
        self.current_view = DashboardView(self.main_container, self.db, self.show_register)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_register(self):
        self.clear_main_container()
        self.current_view = RegisterView(self.main_container, self.db, self.sync_service, self.show_dashboard)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_history(self):
        self.clear_main_container()
        self.current_view = HistoryView(self.main_container, self.db, self.sheets_service)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_records(self):
        self.clear_main_container()
        self.current_view = RecordsView(self.main_container, self.db)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def auto_sync(self):
        try:
            imported_count, pull_msg = self.sync_service.pull_from_sheets_to_sqlite()
            print(f"[PULL]: {pull_msg}")

            success, fail, push_msg = self.sync_service.sync_pending_records()
            print(f"[PUSH]: {push_msg}")

            # Actualizar estado del indicador
            self.after(0, lambda: self.lbl_sync_status.configure(
                text="🟢 Sincronizado", 
                text_color=THEME_COLORS["success"]
            ))

            # Si la vista actual soporta recarga (Dashboard / Historial), refrescar datos
            self.after(0, self.refresh_current_view)

        except Exception as e:
            print(f"[AUTO_SYNC ERROR]: {e}")
            self.after(0, lambda: self.lbl_sync_status.configure(
                text="🔴 Sin Conexión", 
                text_color=THEME_COLORS["error"]
            ))

    def refresh_current_view(self):
        """Redibuja la vista actual para reflejar cambios importados en la base de datos."""
        if isinstance(self.current_view, DashboardView):
            self.show_dashboard()
        elif isinstance(self.current_view, HistoryView):
            self.show_history()

if __name__ == "__main__":
    app = RunningTrackerApp()
    app.mainloop()