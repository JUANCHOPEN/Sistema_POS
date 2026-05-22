from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Datos de conexión
SERVER   = os.getenv("DATABASE_SERVER")
DATABASE = os.getenv("DATABASE_NAME")

# Cadena de conexión a SQL Server con autenticación de Windows
CONNECTION_STRING = (
    f"mssql+pyodbc://{SERVER}/{DATABASE}"
    f"?driver=ODBC+Driver+17+for+SQL+Server"
    f"&trusted_connection=yes"
)

# Crear el motor de conexión
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