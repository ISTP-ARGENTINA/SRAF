import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Conexión a PostgreSQL. Las credenciales salen de variables de entorno
# (con valores por defecto para desarrollo local). RealDictCursor hace que
# cada fila se use como diccionario: fila["columna"].

def obtener_conexion():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "bd_sraf"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "...."),
        cursor_factory=RealDictCursor,
    )
    return conn

def inicializar():
    """
    Crea los tipos ENUM y las tablas si aún no existen.
    Se llama UNA vez al iniciar el sistema.
        CREATE DATABASE bd_sraf;
    """
    conn = obtener_conexion()
    cursor = conn.cursor()

    # ENUMs: CREATE TYPE no soporta IF NOT EXISTS
    # que ignora el error si el tipo ya existe.
    cursor.execute("""
        DO $$ BEGIN
            CREATE TYPE estado_activo_enum AS ENUM ('OPERATIVO', 'EN_REPARACION', 'INACTIVO', 'PRESTADO');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)
    cursor.execute("""
        DO $$ BEGIN
            CREATE TYPE estado_usuario_enum AS ENUM ('ACTIVO', 'INACTIVO', 'BLOQUEADO');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)
    cursor.execute("""
        DO $$ BEGIN
            CREATE TYPE estado_inventario_enum AS ENUM ('ABIERTO', 'EN_PROCESO', 'CERRADO');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)
    cursor.execute("""
        DO $$ BEGIN
            CREATE TYPE tipo_ajuste_enum AS ENUM ('INCREMENTO', 'DISMINUCION', 'CORRECCION');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)

    # Tabla categoria_activo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria_activo (
            id_categoria SERIAL PRIMARY KEY,
            nombre       VARCHAR(100) NOT NULL,
            descripcion  TEXT
        )
    """)

    # Tabla proveedor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedor (
            numero_documento_proveedor VARCHAR(20) PRIMARY KEY,
            tipo_documento              VARCHAR(25) NOT NULL,
            razon_social                VARCHAR(150) NOT NULL,
            telefono                    VARCHAR(20),
            correo                      VARCHAR(100)
        )
    """)

    # Tabla sede
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sede (
            id_sede    SERIAL PRIMARY KEY,
            nombre     VARCHAR(100) NOT NULL,
            direccion  VARCHAR(255) NOT NULL,
            ciudad     VARCHAR(50) NOT NULL
        )
    """)

    # Tabla area
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS area (
            id_area     SERIAL PRIMARY KEY,
            nombre      VARCHAR(100) NOT NULL,
            descripcion TEXT
        )
    """)

    # Tabla usuario. "contraseña" va entre comillas por la ñ:
    # en Postgres hay que usarlas siempre que se consulte esta columna.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario     SERIAL PRIMARY KEY,
            nombres        VARCHAR(100) NOT NULL,
            apellidos      VARCHAR(100) NOT NULL,
            nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
            correo         VARCHAR(100) NOT NULL UNIQUE,
            contrasena     VARCHAR(255) NOT NULL,
            rol            VARCHAR(30) NOT NULL,
            estado         estado_usuario_enum NOT NULL DEFAULT 'ACTIVO',
            fecha_creacion TIMESTAMP NOT NULL DEFAULT NOW(),
            ultimo_acceso  TIMESTAMP
        )
    """)

    # Tabla inventario_fisico. "año" también va entre comillas por la ñ.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario_fisico (
            id_inventario SERIAL PRIMARY KEY,
            anio          INT NOT NULL CHECK ("año" >= 2020),
            fecha_inicio  DATE NOT NULL DEFAULT CURRENT_DATE,
            fecha_fin     DATE,
            estado        estado_inventario_enum NOT NULL DEFAULT 'ABIERTO'
        )
    """)

    # Tabla activo: entidad núcleo, con las 4 llaves foráneas
    # (categoria, proveedor, sede, area).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activo (
            id_activo                  SERIAL PRIMARY KEY,
            codigo_patrimonial         VARCHAR(50) NOT NULL UNIQUE,
            descripcion                VARCHAR(255) NOT NULL,
            marca                      VARCHAR(50),
            modelo                     VARCHAR(50),
            serie                      VARCHAR(50) UNIQUE,
            tipo_comprobante           VARCHAR(20) NOT NULL,
            serie_comprobante          VARCHAR(20) NOT NULL,
            numero_comprobante         VARCHAR(30) NOT NULL,
            fecha_compra               DATE NOT NULL,
            valor_compra               NUMERIC(12, 2) NOT NULL CHECK (valor_compra >= 0.00),
            estado                     estado_activo_enum NOT NULL DEFAULT 'OPERATIVO',
            id_categoria               INT NOT NULL REFERENCES categoria_activo(id_categoria) ON DELETE RESTRICT ON UPDATE CASCADE,
            numero_documento_proveedor VARCHAR(20) NOT NULL REFERENCES proveedor(numero_documento_proveedor) ON DELETE RESTRICT ON UPDATE CASCADE,
            id_sede                    INT NOT NULL REFERENCES sede(id_sede) ON DELETE RESTRICT ON UPDATE CASCADE,
            id_area                    INT NOT NULL REFERENCES area(id_area) ON DELETE RESTRICT ON UPDATE CASCADE
        )
    """)

    # Tabla ajuste_activo: historial de cambios técnicos/económicos de un activo.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ajuste_activo (
            id_ajuste      SERIAL PRIMARY KEY,
            fecha          TIMESTAMP NOT NULL DEFAULT NOW(),
            tipo_ajuste    tipo_ajuste_enum NOT NULL,
            valor_anterior VARCHAR(100) NOT NULL,
            valor_nuevo    VARCHAR(100) NOT NULL,
            observacion    TEXT NOT NULL,
            id_activo      INT NOT NULL REFERENCES activo(id_activo) ON DELETE CASCADE ON UPDATE CASCADE,
            id_usuario     INT NOT NULL REFERENCES usuario(id_usuario) ON DELETE RESTRICT ON UPDATE CASCADE
        )
    """)

    # Tabla baja_activo: expediente de salida definitiva de un activo.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS baja_activo (
            id_baja      SERIAL PRIMARY KEY,
            fecha_baja   DATE NOT NULL DEFAULT CURRENT_DATE,
            motivo       VARCHAR(50) NOT NULL,
            descripcion  TEXT NOT NULL,
            id_activo    INT NOT NULL UNIQUE REFERENCES activo(id_activo) ON DELETE CASCADE ON UPDATE CASCADE,
            id_usuario   INT NOT NULL REFERENCES usuario(id_usuario) ON DELETE RESTRICT ON UPDATE CASCADE
        )
    """)

    # Tabla detalle_inventario: intermedia N:M entre inventario_fisico y activo.
    # El UNIQUE evita escanear el mismo activo dos veces en la misma campaña.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_inventario (
            id_detalle    SERIAL PRIMARY KEY,
            id_inventario INT NOT NULL REFERENCES inventario_fisico(id_inventario) ON DELETE CASCADE ON UPDATE CASCADE,
            id_activo     INT NOT NULL REFERENCES activo(id_activo) ON DELETE RESTRICT ON UPDATE CASCADE,
            encontrado    BOOLEAN NOT NULL DEFAULT TRUE,
            observacion   TEXT,
            CONSTRAINT uq_inventario_activo UNIQUE (id_inventario, id_activo)
        )
    """)

    # Índices para acelerar búsquedas y cruces frecuentes.
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activo_codigo_pat ON activo(codigo_patrimonial)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activo_estado ON activo(estado)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activo_categoria ON activo(id_categoria)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activo_area ON activo(id_area)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ajuste_activo ON ajuste_activo(id_activo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_baja_activo ON baja_activo(id_activo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_detalle_inventario ON detalle_inventario(id_inventario)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_detalle_activo ON detalle_inventario(id_activo)")

    conn.commit()
    cursor.close()
    conn.close()