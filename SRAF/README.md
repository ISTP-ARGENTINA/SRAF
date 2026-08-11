SRAF - Sistema de Registro de Activos Fijos

API REST construida con FastAPI y PostgreSQL para el registro y control de activos fijos, sedes, áreas, proveedores, categorías, usuarios, inventarios físicos, ajustes y bajas de activos.

Requisitos previos
Python 3.11 o superior
PostgreSQL instalado y corriendo
Git
1. Clonar el repositorio
bash
git clone <URL_DEL_REPOSITORIO>
cd SRAF

⚠️ Verifica que quedes en la carpeta donde está main.py. Si al clonar se crea una carpeta anidada (por ejemplo SRAF/SRAF), entra un nivel más con cd SRAF.

2. Crear y activar un entorno virtual

Windows (PowerShell):

powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

Mac/Linux:

bash
python3 -m venv venv
source venv/bin/activate

Sabrás que está activo porque el prompt cambia a (venv) ....

3. Instalar las dependencias
bash
pip install -r requirements.txt

Si no existe requirements.txt todavía, instala manualmente y luego genera el archivo:

bash
pip install fastapi uvicorn[standard] psycopg2-binary pydantic python-dotenv
pip freeze > requirements.txt
4. Crear la base de datos en PostgreSQL

Conéctate a PostgreSQL:

bash
psql -U postgres

(en Windows, si psql no se reconoce, usa la ruta completa, por ejemplo: & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres)

Dentro de psql, crea la base de datos:

sql
CREATE DATABASE bd_sraf;

Sal con:

sql
\q

El nombre debe ser bd_sraf en minúsculas. Si la creaste en mayúsculas por accidente, renómbrala con ALTER DATABASE "BD_SRAF" RENAME TO bd_sraf;.

5. Configurar las variables de entorno

Crea un archivo .env en la raíz del proyecto (junto a main.py) con este contenido:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=bd_sraf
DB_USER=postgres
DB_PASSWORD=tu_contraseña_de_postgres

Reemplaza tu_contraseña_de_postgres por la contraseña real de tu usuario postgres.

Variable	Descripción
DB_HOST	Host de PostgreSQL (localhost en desarrollo local)
DB_PORT	Puerto de PostgreSQL (5432 por defecto)
DB_NAME	Nombre de la base de datos (bd_sraf)
DB_USER	Usuario de PostgreSQL
DB_PASSWORD	Contraseña de ese usuario

🔒 El archivo .env nunca debe subirse a git — agrégalo a .gitignore si no está ya.

6. Levantar el servidor
bash
uvicorn main:app --reload

Si uvicorn no se reconoce como comando (típico en Windows si el Scripts del venv no está en el PATH):

bash
python -m uvicorn main:app --reload

Si todo salió bien, verás:

INFO:     Application startup complete.

Esto significa que el servidor se conectó a la base de datos y creó las tablas automáticamente la primera vez (vía inicializar() en config/base_datos.py).

7. Verificar que funciona

Abre en el navegador:

http://127.0.0.1:8000/docs

Deberías ver la documentación interactiva (Swagger) con todos los endpoints: categorías, proveedores, sedes, áreas, usuarios, activos, inventarios, ajustes, bajas, y detalles de inventario.

Si en cambio dice "No operations defined in spec!", revisa que main.py tenga las líneas app.include_router(...) para cada router.

Estructura del proyecto
SRAF/
├── main.py             # Punto de entrada: crea la app y conecta los routers
├── routers/             # Endpoints HTTP (uno por entidad)
├── schemas/             # Validación de datos de entrada/salida (Pydantic)
├── dao/                 # Acceso a datos: ejecuta las consultas SQL
├── modelos/              # Clases de datos planas (representan cada entidad)
├── config/
│   ├── base_datos.py     # Conexión a PostgreSQL y creación de tablas
│   ├── sistema_config.py # Singleton de configuración + excepciones del negocio
│   └── logger.py          # Singleton de logging propio
├── requirements.txt
├── .env                  # Variables de entorno (no se sube a git)
└── .gitignore

Las dependencias entre capas van en una sola dirección:

routers → schemas / dao / modelos
dao → config / modelos
Problemas comunes
Síntoma	Causa probable	Solución
uvicorn no se reconoce como comando	El entorno virtual no está activado, o el Scripts folder no está en el PATH	Usa python -m uvicorn main:app --reload
ModuleNotFoundError: No module named 'fastapi' (u otro paquete)	Faltan dependencias instaladas	pip install -r requirements.txt (con el venv activado)
psycopg2.OperationalError: ... no password supplied	Falta el archivo .env, o no tiene DB_PASSWORD	Crea el .env con la contraseña real de PostgreSQL
ImportError: cannot import name 'X' from 'config.sistema_config'	Falta esa excepción, o hay un typo en el nombre importado	Revisa que el nombre coincida exactamente con el definido en sistema_config.py
column "X" of relation "Y" does not exist	Nombre de columna con tilde/ñ inconsistente entre config/base_datos.py y el DAO (ej. año vs anio, contraseña vs contrasena)	Unifica el nombre en ambos lados; se recomienda evitar tildes/ñ en identificadores SQL
El servidor arranca pero /docs dice "No operations defined in spec!"	Falta registrar los routers en main.py	Verifica que existan las líneas app.include_router(...) para cada router
Carpeta del proyecto anidada (SRAF/SRAF/...)	Se clonó el repo dentro de una carpeta que ya se llamaba igual	cd a la subcarpeta que contiene main.py
AttributeError: 'XxxDAO' object has no attribute 'buscar_por_id'	El DAO relacionado no tiene ese método, pero ActivoDAO (u otro) lo necesita para validar llaves foráneas	Agregar el método buscar_por_id() a ese DAO
Autor

Sistema desarrollado para ISTP ARGENTINA — Sistema de Registro de Activos Fijos (SRAF) v1.0

Pasos:

Busca "Variables de entorno" en el menú de inicio → "Editar las variables de entorno del sistema"
Clic en "Variables de entorno..."
En la sección de usuario (arriba), selecciona la variable Path → "Editar" → "Nuevo"
Pega: C:\Program Files\PostgreSQL\18\bin
Acepta todo
Cierra completamente PowerShell y vuelve a abrirlo (importante, si no, no toma el cambio)cd C:\Users\HP G42\Desktop\SRAF\SRAF
.\venv\Scripts\Activate.ps1

$env:Path -split ';' | Select-String "PostgreSQL"

cd C:\Users\HP G42\Desktop\SRAF\SRAF
.\venv\Scripts\Activate.ps1