# 🏃‍♂️ Running Tracker Desktop

Aplicación de escritorio desarrollada en Python para el seguimiento y registro de sesiones de carrera. Permite almacenar datos localmente mediante **SQLite** y sincronizar registros de forma automática con **Google Sheets**.

---

## 🚀 Características

* **Registro Local Rápido**: Almacenamiento directo en base de datos SQLite para consulta offline.
* **Sincronización Cloud**: Integración bidireccional mediante la API de Google Sheets (`gspread`).
* **Estado de Sincronización**: Control mediante bandera (`is_synced`) para operar con o sin conexión a internet.
* **Interfaz de Usuario**: Módulos para registro de carreras, historial completo, métricas de marcas personales y panel de estadísticas.

---

## 🛠️ Requisitos Previos

* Python 3.10 o superior.
* Una cuenta de Google Cloud Console con la API de **Google Sheets** habilitada y un **Service Account**.

---

## 📦 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone git@github.com-personal:ROMeO-OWL/RunningTracker.git
   cd RunningTracker