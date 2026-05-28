import pyodbc
from passlib.context import CryptContext

SERVER = "localhost"
DATABASE = "SistemaPOS"
DRIVER = "{ODBC Driver 17 for SQL Server}"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

admin_hash = pwd_context.hash("admin123")
cajero_hash = pwd_context.hash("cajero123")

master_conn = pyodbc.connect(
f"DRIVER={DRIVER};SERVER={SERVER};DATABASE=master;Trusted_Connection=yes;",
autocommit=True
)

master_cursor = master_conn.cursor()
master_cursor.execute("IF DB_ID(N'SistemaPOS') IS NULL CREATE DATABASE SistemaPOS")
master_conn.close()

conn = pyodbc.connect(
f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
)

cursor = conn.cursor()

cursor.execute("""
IF OBJECT_ID('PRODUCTO', 'U') IS NOT NULL DROP TABLE PRODUCTO;
IF OBJECT_ID('CATEGORIA', 'U') IS NOT NULL DROP TABLE CATEGORIA;
IF OBJECT_ID('USUARIO', 'U') IS NOT NULL DROP TABLE USUARIO;
IF OBJECT_ID('ROL', 'U') IS NOT NULL DROP TABLE ROL;

CREATE TABLE ROL (
id_rol INT IDENTITY(1,1) PRIMARY KEY,
nombre VARCHAR(50) NOT NULL,
descripcion VARCHAR(200) NULL
);

CREATE TABLE USUARIO (
id_usuario INT IDENTITY(1,1) PRIMARY KEY,
id_rol INT NOT NULL,
nombre_completo VARCHAR(150) NOT NULL,
correo VARCHAR(150) NOT NULL UNIQUE,
contrasena_hash VARCHAR(255) NOT NULL,
activo BIT NOT NULL DEFAULT 1,
fecha_creacion DATETIME2 NOT NULL DEFAULT GETDATE(),
ultimo_acceso DATETIME2 NULL,
intentos_fallidos SMALLINT NOT NULL DEFAULT 0,
CONSTRAINT FK_USUARIO_ROL FOREIGN KEY (id_rol) REFERENCES ROL(id_rol)
);

CREATE TABLE CATEGORIA (
id_categoria INT IDENTITY(1,1) PRIMARY KEY,
nombre VARCHAR(100) NOT NULL UNIQUE,
descripcion VARCHAR(255) NULL
);

CREATE TABLE PRODUCTO (
id_producto INT IDENTITY(1,1) PRIMARY KEY,
id_categoria INT NOT NULL,
codigo VARCHAR(50) NOT NULL UNIQUE,
nombre VARCHAR(200) NOT NULL,
precio_venta DECIMAL(10,2) NOT NULL,
precio_costo DECIMAL(10,2) NOT NULL,
stock_actual INT NOT NULL DEFAULT 0,
stock_minimo INT NOT NULL DEFAULT 5,
activo BIT NOT NULL DEFAULT 1,
fecha_creacion DATETIME2 NOT NULL DEFAULT GETDATE(),
CONSTRAINT FK_PRODUCTO_CATEGORIA FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria)
);
""")

cursor.execute("INSERT INTO ROL (nombre, descripcion) VALUES (?, ?)", "Administrador", "Acceso completo al sistema")
cursor.execute("INSERT INTO ROL (nombre, descripcion) VALUES (?, ?)", "Cajero", "Acceso operativo al punto de venta")

cursor.execute("INSERT INTO USUARIO (id_rol, nombre_completo, correo, contrasena_hash, activo, intentos_fallidos) VALUES (?, ?, ?, ?, ?, ?)", 1, "Administrador General", "admin@pos.gt", admin_hash, 1, 0)
cursor.execute("INSERT INTO USUARIO (id_rol, nombre_completo, correo, contrasena_hash, activo, intentos_fallidos) VALUES (?, ?, ?, ?, ?, ?)", 2, "Cajero Demo", "cajero@pos.gt", cajero_hash, 1, 0)

cursor.execute("INSERT INTO CATEGORIA (nombre, descripcion) VALUES (?, ?)", "Bebidas", "Productos liquidos")
cursor.execute("INSERT INTO CATEGORIA (nombre, descripcion) VALUES (?, ?)", "Abarrotes", "Productos de consumo diario")
cursor.execute("INSERT INTO CATEGORIA (nombre, descripcion) VALUES (?, ?)", "Limpieza", "Productos de limpieza")

cursor.execute("INSERT INTO PRODUCTO (id_categoria, codigo, nombre, precio_venta, precio_costo, stock_actual, stock_minimo, activo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 1, "BEB-001", "Agua pura 600ml", 5.00, 3.00, 35, 10, 1)
cursor.execute("INSERT INTO PRODUCTO (id_categoria, codigo, nombre, precio_venta, precio_costo, stock_actual, stock_minimo, activo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 1, "BEB-002", "Gaseosa lata", 7.50, 5.00, 18, 8, 1)
cursor.execute("INSERT INTO PRODUCTO (id_categoria, codigo, nombre, precio_venta, precio_costo, stock_actual, stock_minimo, activo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 2, "ABA-001", "Arroz blanco 1lb", 6.00, 4.00, 40, 10, 1)
cursor.execute("INSERT INTO PRODUCTO (id_categoria, codigo, nombre, precio_venta, precio_costo, stock_actual, stock_minimo, activo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 2, "ABA-002", "Frijol negro 1lb", 8.00, 5.50, 6, 10, 1)
cursor.execute("INSERT INTO PRODUCTO (id_categoria, codigo, nombre, precio_venta, precio_costo, stock_actual, stock_minimo, activo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 3, "LIM-001", "Jabon antibacterial", 12.00, 8.00, 4, 5, 1)

conn.commit()
conn.close()

print("Base SistemaPOS creada correctamente")
print("Usuario admin: admin@pos.gt")
print("Password admin: admin123")
print("Usuario cajero: cajero@pos.gt")
print("Password cajero: cajero123")
