# 🏃‍♂️ Running Tracker Desktop

Aplicación de escritorio desarrollada en Python para el seguimiento y registro de carreras. Permite almacenar datos localmente mediante **SQLite** y sincronizar registros de forma automática con tu propia hoja de **Google Sheets**.

---

## 🚀 Características

* **Registro Local Rápido**: Almacenamiento directo en base de datos SQLite.
* **Sincronización Cloud Privada**: Integración mediante la API de Google Sheets (`gspread`) usando tu propio Service Account.
* **Modo Offline**: Control de estado (`is_synced`) para registrar carreras sin conexión a internet.
* **Interfaz de Usuario**: Panel para visualizar estadísticas, historial y métricas.

---

## 🛠️ Requisitos Previos

1. Python 3.10 o superior.
2. Una cuenta de Google.

---

## 🔑 Configuración de Credenciales de Google (Paso a Paso)

Para que la aplicación se conecte a tu propia hoja de cálculo, debes obtener tus credenciales gratuitas de Google Cloud:

### Paso 1: Crear el proyecto y activar la API
1. Ve a [Google Cloud Console](https://console.cloud.google.com/).
2. Crea un nuevo proyecto (ej. `Mi-Running-Tracker`).
3. En el menú lateral, ve a **APIs y servicios** > **Biblioteca**
4. Busca **Google Sheets API** y haz clic en **Habilitar**.

### Paso 2: Crear la cuenta de servicio (Service Account)
1. Ve a **APIs y servicios** > **Credenciales**
2. Haz clic en **Crear credenciales** > **Cuenta de servicio**
3. Asigna un nombre (ej. `running-tracker-service`) y haz clic en **Crear y continuar**
4. En el paso de roles, selecciona **Editor** (o déjalo en blanco) y haz clic en **Listo**

### Paso 3: Descargar el archivo de credenciales JSON
1. En la lista de **Cuentas de servicio**, haz clic sobre el correo recién creado
2. Ve a la pestaña **Claves** (Keys) > **Agregar clave** > **Crear clave nueva**
3. Selecciona el formato **JSON** y haz clic en **Crear**. Se descargará un archivo `.json` a tu equipo
4. Renombra ese archivo descargado exactamente a `credentials.json`

---

## 📦 Instalación y Configuración del Proyecto

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/ROMeO-OWL/RunningTracker.git](https://github.com/ROMeO-OWL/RunningTracker.git)
   cd RunningTracker

2. **Crear y activar el entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux / macOS:
   source venv/bin/activate

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt

4. **Ubicación de las credenciales de Google**:
   * Crea una carpeta llamada `credentials` en la raíz del proyecto (si no existe)
   * Mueve tu archivo `credentials.json` descargado dentro de esa carpeta: `credentials/credentials.json`

5. **Configurar la Hoja de Google Sheets**:
   * Entra a [Google Sheets](https://sheets.google.com) y crea una **nueva hoja de cálculo en blanco**
   * Ponle de nombre a la pestaña principal: `Running`.
   * **Importante**: Abre tu archivo `credentials.json`, copia la dirección de correo que está en `"client_email"` (ej. `running-tracker@...iam.gserviceaccount.com`).
   * En tu hoja de Google Sheets, haz clic en **Compartir** y agrega ese correo de la cuenta de servicio con permisos de **Editor**

6. **Configurar Variables de Entorno (`.env`)**:
   * Copia la plantilla de variables de entorno

     cp .env.example .env

   * Abre el archivo `.env` en un editor de texto y coloca el **ID de tu hoja de cálculo** (lo encuentras en la URL de tu hoja entre `/d/` y `/edit`):
     ```ini
     GOOGLE_SHEET_ID=tu_id_de_google_sheet_aqui
     GOOGLE_SHEET_NAME=Running

---

## 💻 Ejecución

Con las credenciales y el archivo `.env` listos, inicia la aplicación:

python main.py

## ⚙️ Generar Ejecutable Portable (.exe) con PyInstaller

Para empaquetar la aplicación en un `.exe` totalmente independiente para Windows (incluyendo entornos `.env`, credenciales, recursos e importaciones dinámicas), ejecuta el siguiente comando:
```bash
### 1. Instalar PyInstaller
pip install pyinstaller

### 2. .exe
pyinstaller --noconfirm --onedir --windowed --icon="ui/assets/app_icon.ico" --hidden-import="unicodedata" --hidden-import="certifi" --hidden-import="google.oauth2.service_account" --hidden-import="gspread" --add-data ".env;." --add-data "credentials/credentials.json;credentials" --add-data "ui/assets/app_icon.ico;ui/assets" main.py

### 3. Ubicacion del .exe
dist/main/main.exe
