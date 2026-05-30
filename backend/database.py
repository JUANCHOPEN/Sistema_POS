from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Datos de conexión
# Cargar variables del archivo .env (solo sirve en local)
load_dotenv()

# 1. Intentamos leer la variable 'DATABASE_URL' que configuraremos en Render de forma secreta
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Corrección obligatoria: Render/PostgreSQL exige que la cadena empiece con 'postgresql://' y no 'postgres://'
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Si detecta la URL de la nube, creamos el motor para PostgreSQL
    engine = create_engine(DATABASE_URL)
else:
    # 2. Si no existe DATABASE_URL (significa que estás corriendo el código en tu computadora local)
    # Mantiene tu configuración original de SQL Server
    SERVER   = os.getenv("DATABASE_SERVER")
    DATABASE = os.getenv("DATABASE_NAME")
    
    CONNECTION_STRING = (
        f"mssql+pyodbc://{SERVER}/{DATABASE}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
        f"&trusted_connection=yes"
    )
    engine = create_engine(CONNECTION_STRING)
# Crear sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar la conexión
def verificar_conexion():
    try:
        with engine.connect() as conexion:
            conexion.execute(text("SELECT 1"))
            print("✅ Conexión a SQL Server exitosa")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
