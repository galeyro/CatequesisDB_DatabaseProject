# CatequesisDB - Sistema de Gestión de Catequesis

Sistema de gestión para parroquias que permite administrar alumnos, catequistas y grupos de catequesis. El proyecto implementa una arquitectura híbrida soportando bases de datos SQL (SQL Server) y NoSQL (MongoDB), con autenticación centralizada mediante Keycloak.

## 👥 Autores
- **Galo Guevara**
- **Eduardo Andrade**
- **Javier Arias**

---

## 🚀 Características Principales
*   **Gestión de Alumnos**: Información personal, representantes y sacramentos.
*   **Gestión de Catequistas**: Asignación a grupos y datos de contacto.
*   **Gestión de Grupos**: Organización por niveles y periodos lectivos.
*   **Doble Persistencia**:
    *   **SQL Server**: Para datos estructurados y reportes tradicionales.
    *   **MongoDB**: Para estructuras flexibles, historial de sacramentos y documentos anidados.
*   **Seguridad**: Autenticación OAuth2 / OpenID Connect integrada con **Keycloak**.

---

## 🛠️ Requisitos Previos
*   Python 3.10+
*   SQL Server (para la base relacional)
*   MongoDB (para la base NoSQL)
*   Keycloak (corriendo en `localhost:8080` u otro servidor configurado)

---

## 📦 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd Fase7-BD
```

### 2. Crear y Activar Entorno Virtual (venv)
Es recomendable usar un entorno virtual para aislar las dependencias.

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux / Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
Las librerías necesarias para el proyecto son:

*   `Django`: Framework web principal.
*   `pymongo`: Driver para conectar con MongoDB.
*   `mssql-django`: Backend de base de datos para Microsoft SQL Server.
*   `mozilla-django-oidc`: Integración para autenticación con Keycloak.
*   `python-dotenv`: Para manejo de variables de entorno.
*   `requests`: Utilidad para peticiones HTTP.

Puedes instalarlas manualmente o usando `pip` si tienes un archivo de requisitos (se recomienda crear uno con `pip freeze > requirements.txt`):

```bash
pip install django pymongo mssql-django mozilla-django-oidc python-dotenv requests
```

### 4. Configurar Variables de Entorno (.env)
Crea un archivo `.env` en la raíz del proyecto (`DjangoCatequesis/.env`) con la siguiente configuración:

```ini
# Configuración Django
SECRET_KEY=tu_clave_secreta_segura
DEBUG=True

# Autenticación Keycloak
KEYCLOAK_CLIENT_ID=django-app
KEYCLOAK_CLIENT_SECRET=tu_client_secret_de_keycloak
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=CatequesisDB

# Base de Datos SQL (SQL Server)
SQL_SERVER=localhost
SQL_DB=CatequesisSQL
SQL_USER=sa
SQL_PASSWORD=tu_password_sql

# Base de Datos NoSQL (MongoDB)
MONGO_URI=mongodb://localhost:27017/
```

### 5. Migraciones
Para inicializar la estructura de la base de datos SQL:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Poblar Datos de Prueba (NoSQL)
El proyecto incluye un script para generar datos dummy en MongoDB para pruebas:

```bash
python populate_nosql.py
```
*Nota: Este script limpiará las colecciones de MongoDB y creará nuevos registros de prueba.*

### 7. Ejecutar el Servidor
```bash
python manage.py runserver
```
Accede a `http://localhost:8000`.

---

## 🔐 Autenticación con Keycloak
El sistema delega el login a Keycloak.
1.  Al intentar ingresar a una zona protegida, serás redirigido al login de Keycloak.
2.  Ingresa tus credenciales (usuario/password configurados en tu Realm).
3.  Al autenticarte exitosamente, serás redirigido de vuelta al **Dashboard** de la aplicación.

Asegúrate de configurar en Keycloak:
*   **Valid Redirect URIs**: `http://localhost:8000/*`

---

## 📂 Estructura del Proyecto
*   `DjangoCatequesis/`: Configuración principal del proyecto.
*   `templates/`: Plantillas HTML (incluye carpetas `nosql/` y `catalogos/`).
*   `views.py`: Lógica para vistas SQL.
*   `views_nosql.py`: Lógica específica para vistas y operaciones MongoDB.
*   `utils_mongo.py`: Helper de conexión a MongoDB.
