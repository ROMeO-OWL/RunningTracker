# 🏃‍♂️ Running Tracker Desktop

Aplicación de escritorio desarrollada en Python para el seguimiento y registro de carreras. Permite almacenar datos localmente mediante **SQLite** y sincronizar registros de forma automática con tu propia hoja de **Google Sheets**[cite: 1].

---

## 🚀 Características

* **Registro Local Rápido**: Almacenamiento directo en base de datos SQLite[cite: 1].
* **Sincronización Cloud Privada**: Integración mediante la API de Google Sheets (`gspread`) usando tu propio Service Account[cite: 1].
* **Modo Offline**: Control de estado (`is_synced`) para registrar carreras sin conexión a internet[cite: 1].
* **Interfaz de Usuario**: Panel para visualizar estadísticas, historial y métricas[cite: 1].

---

## 🛠️ Requisitos Previos

1. Python 3.10 o superior[cite: 1].
2. Una cuenta de Google[cite: 1].

---

## 🔑 Configuración de Credenciales de Google (Paso a Paso)

Para que la aplicación se conecte a tu propia hoja de cálculo, debes obtener tus credenciales gratuitas de Google Cloud[cite: 1]:

### Paso 1: Crear el proyecto y activar la API
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)[cite: 1].
2. Crea un nuevo proyecto (ej. `Mi-Running-Tracker`)[cite: 1].
3. En el menú lateral, ve a **APIs y servicios** > **Biblioteca**[cite: 1].
4. Busca **Google Sheets API** y haz clic en **Habilitar**[cite: 1].

### Paso 2: Crear la cuenta de servicio (Service Account)
1. Ve a **APIs y servicios** > **Credenciales**[cite: 1].
2. Haz clic en **Crear credenciales** > **Cuenta de servicio**[cite: 1].
3. Asigna un nombre (ej. `running-tracker-service`) y haz clic en **Crear y continuar**[cite: 1].
4. En el paso de roles, selecciona **Editor** (o déjalo en blanco) y haz clic en **Listo**[cite: 1].

### Paso 3: Descargar el archivo de credenciales JSON
1. En la lista de **Cuentas de servicio**, haz clic sobre el correo recién creado[cite: 1].
2. Ve a la pestaña **Claves** (Keys) > **Agregar clave** > **Crear clave nueva**[cite: 1].
3. Selecciona el formato **JSON** y haz clic en **Crear**. Se descargará un archivo `.json` a tu equipo[cite: 1].
4. Renombra ese archivo descargado exactamente a `credentials.json`[cite: 1].

---

## 📦 Instalación y Configuración del Proyecto

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/ROMeO-OWL/RunningTracker.git](https://github.com/ROMeO-OWL/RunningTracker.git)
   cd RunningTracker
   ```[cite: 1]

2. **Crear y activar el entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux / macOS:
   source venv/bin/activate
   ```[cite: 1]

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```[cite: 1]

4. **Ubicación de las credenciales de Google**:
   * Crea una carpeta llamada `credentials` en la raíz del proyecto (si no existe)[cite: 1].
   * Mueve tu archivo `credentials.json` descargado dentro de esa carpeta: `credentials/credentials.json`[cite: 1].

5. **Configurar la Hoja de Google Sheets**:
   * Entra a [Google Sheets](https://sheets.google.com) y crea una **nueva hoja de cálculo en blanco**[cite: 1].
   * Ponle de nombre a la pestaña principal: `Running`[cite: 1].
   * **Importante**: Abre tu archivo `credentials.json`, copia la dirección de correo que está en `"client_email"` (ej. `running-tracker@...iam.gserviceaccount.com`)[cite: 1].
   * En tu hoja de Google Sheets, haz clic en **Compartir** y agrega ese correo de la cuenta de servicio con permisos de **Editor**[cite: 1].

6. **Configurar Variables de Entorno (`.env`)**:
   * Copia la plantilla de variables de entorno:
     ```bash
     cp .env.example .env
     ```[cite: 1]
   * Abre el archivo `.env` en un editor de texto y coloca el **ID de tu hoja de cálculo** (lo encuentras en la URL de tu hoja entre `/d/` y `/edit`)[cite: 1]:
     ```ini
     GOOGLE_SHEET_ID=tu_id_de_google_sheet_aqui
     GOOGLE_SHEET_NAME=Running
     ```[cite: 1]

---

## 💻 Ejecución

Con las credenciales y el archivo `.env` listos, inicia la aplicación:

```bash
python main.py
```[cite: 1]

---

## ⚙️ Generar Ejecutable Portable (.exe) con PyInstaller

Para empaquetar la aplicación en un `.exe` totalmente independiente para Windows (incluyendo entornos `.env`, credenciales, recursos e importaciones dinámicas), ejecuta el siguiente comando:

### 1. Instalar PyInstaller
```bash
pip install pyinstaller

### 2. .exe
```bash
pyinstaller --noconfirm --onedir --windowed --icon="ui/assets/app_icon.ico" --hidden-import="unicodedata" --hidden-import="certifi" --hidden-import="google.oauth2.service_account" --hidden-import="gspread" --add-data ".env;." --add-data "credentials/credentials.json;credentials" --add-data "ui/assets/app_icon.ico;ui/assets" main.py

### 3. Ubicacion del .exe
```bash
dist/main/main.exe
