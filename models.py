from database import get_db
from datetime import datetime, timedelta
import sqlite3

class Usuario:
    @staticmethod
    def crear(username, email, password, nombre, es_admin=False):
        """Crear un nuevo usuario"""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuarios (username, email, password, nombre, es_admin)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password, nombre, es_admin))
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            db.close()
    
    @staticmethod
    def obtener_por_username(username):
        """Obtener usuario por nombre de usuario"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        usuario = cursor.fetchone()
        db.close()
        return dict(usuario) if usuario else None
    
    @staticmethod
    def obtener_por_email(email):
        """Obtener usuario por email"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        db.close()
        return dict(usuario) if usuario else None

class Servicio:
    @staticmethod
    def crear(nombre, descripcion, precio, duracion_minutos=60, imagen=None):
        """Crear nuevo servicio"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO servicios (nombre, descripcion, precio, duracion_minutos, imagen)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, precio, duracion_minutos, imagen))
        db.commit()
        db.close()
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los servicios activos"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM servicios WHERE activo = 1')
        servicios = cursor.fetchall()
        db.close()
        return [dict(s) for s in servicios]
    
    @staticmethod
    def obtener_por_id(id):
        """Obtener servicio por ID"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM servicios WHERE id = ?', (id,))
        servicio = cursor.fetchone()
        db.close()
        return dict(servicio) if servicio else None

class Producto:
    @staticmethod
    def crear(nombre, descripcion, precio, categoria, stock=0, imagen=None):
        """Crear nuevo producto"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, categoria, stock, imagen)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, precio, categoria, stock, imagen))
        db.commit()
        db.close()
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los productos activos"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM productos WHERE activo = 1 ORDER BY fecha_creacion DESC')
        productos = cursor.fetchall()
        db.close()
        return [dict(p) for p in productos]
    
    @staticmethod
    def obtener_por_categoria(categoria):
        """Obtener productos por categoría"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM productos WHERE categoria = ? AND activo = 1', (categoria,))
        productos = cursor.fetchall()
        db.close()
        return [dict(p) for p in productos]
    
    @staticmethod
    def obtener_por_id(id):
        """Obtener producto por ID"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
        producto = cursor.fetchone()
        db.close()
        return dict(producto) if producto else None
    
    @staticmethod
    def actualizar_stock(id, cantidad):
        """Actualizar stock de un producto"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE productos SET stock = stock + ? WHERE id = ?', (cantidad, id))
        db.commit()
        db.close()

class Cita:
    @staticmethod
    def crear(nombre_cliente, email_cliente, telefono_cliente, nombre_mascota, raza, 
              fecha_cita, hora_cita, servicio_id, notas=''):
        """Crear nueva cita"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO citas (nombre_cliente, email_cliente, telefono_cliente, nombre_mascota, 
                             raza, fecha_cita, hora_cita, servicio_id, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre_cliente, email_cliente, telefono_cliente, nombre_mascota, raza,
              fecha_cita, hora_cita, servicio_id, notas))
        db.commit()
        cita_id = cursor.lastrowid
        db.close()
        return cita_id
    
    @staticmethod
    def obtener_todas():
        """Obtener todas las citas"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT c.*, s.nombre as servicio_nombre, s.precio
            FROM citas c
            LEFT JOIN servicios s ON c.servicio_id = s.id
            ORDER BY c.fecha_cita DESC, c.hora_cita DESC
        ''')
        citas = cursor.fetchall()
        db.close()
        return [dict(c) for c in citas]
    
    @staticmethod
    def obtener_por_fecha(fecha):
        """Obtener citas por fecha"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT c.*, s.nombre as servicio_nombre
            FROM citas c
            LEFT JOIN servicios s ON c.servicio_id = s.id
            WHERE c.fecha_cita = ? AND c.estado = 'confirmada'
            ORDER BY c.hora_cita
        ''', (fecha,))
        citas = cursor.fetchall()
        db.close()
        return [dict(c) for c in citas]
    
    @staticmethod
    def actualizar_estado(id, nuevo_estado):
        """Actualizar estado de una cita"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE citas SET estado = ? WHERE id = ?', (nuevo_estado, id))
        db.commit()
        db.close()

class HorarioDisponible:
    @staticmethod
    def crear(dia_semana, hora_inicio, hora_fin):
        """Crear horario disponible"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO horarios_disponibles (dia_semana, hora_inicio, hora_fin)
            VALUES (?, ?, ?)
        ''', (dia_semana, hora_inicio, hora_fin))
        db.commit()
        db.close()
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los horarios"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM horarios_disponibles WHERE activo = 1')
        horarios = cursor.fetchall()
        db.close()
        return [dict(h) for h in horarios]
    
    @staticmethod
    def obtener_por_dia(dia_semana):
        """Obtener horarios para un día específico"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM horarios_disponibles WHERE dia_semana = ? AND activo = 1', (dia_semana,))
        horarios = cursor.fetchall()
        db.close()
        return [dict(h) for h in horarios]

class Galeria:
    @staticmethod
    def crear(titulo, imagen_antes, imagen_despues, descripcion=''):
        """Crear entrada de galería"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO galeria (titulo, imagen_antes, imagen_despues, descripcion)
            VALUES (?, ?, ?, ?)
        ''', (titulo, imagen_antes, imagen_despues, descripcion))
        db.commit()
        db.close()
    
    @staticmethod
    def obtener_todas():
        """Obtener todas las galerías"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM galeria ORDER BY fecha_creacion DESC')
        galerias = cursor.fetchall()
        db.close()
        return [dict(g) for g in galerias]

class Mensaje:
    @staticmethod
    def crear(nombre, email, asunto, mensaje):
        """Crear nuevo mensaje de contacto"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO mensajes (nombre, email, asunto, mensaje)
            VALUES (?, ?, ?, ?)
        ''', (nombre, email, asunto, mensaje))
        db.commit()
        db.close()
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los mensajes"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM mensajes ORDER BY fecha_creacion DESC')
        mensajes = cursor.fetchall()
        db.close()
        return [dict(m) for m in mensajes]
    
    @staticmethod
    def marcar_leido(id):
        """Marcar mensaje como leído"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE mensajes SET leido = 1 WHERE id = ?', (id,))
        db.commit()
        db.close()
