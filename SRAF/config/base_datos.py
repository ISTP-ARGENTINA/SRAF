import pyodbc

SERVIDOR = "localhost"
BASDE_DATOS = "BD_SRAF"
USUARIO = ""
CONTRASEÑA = ""

def obtener_conexion():
    
    conexion = pyodbc.connect(
        f"DRIVE={{ODBC Drive 17 for SQL Server}};"
        f"SERVER={{DESKTOP-KN5K37E\\SQLEXPRESS}};"
        f"DATABASE=BD_SRAF"
        f"Trusted_Connection=yes;"
    )
    
    return conexion