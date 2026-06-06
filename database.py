import os
import sqlite3
from datetime import datetime

# Base de datos SQLite
DATABASE = 'patitas_limpias.db'

def get_db():
    """Obtener conexión a la base de datos"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Inicializar la base de datos con las tablas"""
    db = get_db()
    cursor = db.cursor()
    
    # Tabla de usuarios/administrador
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nombre TEXT NOT NULL,
        es_admin BOOLEAN DEFAULT 0,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        activo BOOLEAN DEFAULT 1
    )
    ''')
    
    # Tabla de servicios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        duracion_minutos INTEGER DEFAULT 60,
        imagen TEXT,
        activo BOOLEAN DEFAULT 1,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        stock INTEGER DEFAULT 0,
        categoria TEXT,
        imagen TEXT,
        activo BOOLEAN DEFAULT 1,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla de citas/reservas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_cliente TEXT NOT NULL,
        email_cliente TEXT,
        telefono_cliente TEXT,
        nombre_mascota TEXT NOT NULL,
        raza TEXT,
        fecha_cita DATE NOT NULL,
        hora_cita TIME NOT NULL,
        servicio_id INTEGER NOT NULL,
        estado TEXT DEFAULT 'confirmada',
        notas TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    )
    ''')
    
    # Tabla de horarios disponibles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS horarios_disponibles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dia_semana TEXT NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fin TIME NOT NULL,
        activo BOOLEAN DEFAULT 1
    )
    ''')
    
    # Tabla de galería antes/después
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS galeria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        imagen_antes TEXT,
        imagen_despues TEXT,
        descripcion TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla de mensajes de contacto
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL,
        asunto TEXT,
        mensaje TEXT NOT NULL,
        leido BOOLEAN DEFAULT 0,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla de carrito
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carrito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER DEFAULT 1,
        fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')
    
    # Tabla de pedidos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_pedido TEXT UNIQUE NOT NULL,
        cliente_nombre TEXT NOT NULL,
        cliente_email TEXT NOT NULL,
        cliente_telefono TEXT,
        total REAL NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_entrega TIMESTAMP
    )
    ''')
    
    db.commit()
    db.close()

# Ejecutar inicialización
if __name__ == '__main__':
    init_db()
    print("✅ Base de datos inicializada correctamente")
