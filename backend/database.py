from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

SERVER = os.getenv("DATABASE_SERVER")
DATABASE = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DRIVER = os.getenv("DATABASE_DRIVER", "ODBC Driver 18 for SQL Server")

connection_url = (
    f"DRIVER={{{DATABASE_DRIVER}}};"
    f"SERVER={SERVER},1433;"
    f"DATABASE={DATABASE};"
    f"UID={DATABASE_USER};"
    f"PWD={DATABASE_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
    f"Connection Timeout=30;"
)

CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_url)}"

engine = create_engine(CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_conexion():
    try:
        with engine.connect() as conexion:
            conexion.execute(text("SELECT 1"))
            print("Conexion a Azure SQL exitosa")
    except Exception as e:
        print(f"Error de conexion a Azure SQL: {e}")