from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os

# Importar configuración
from config import DevelopmentConfig
from database import init_db
from models import Servicio, Producto, Cita, Mensaje, Usuario, HorarioDisponible, Galeria
from utils import login_required, admin_required, save_upload_file, enviar_whatsapp, enviar_email
from routes_admin import admin_bp

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Registrar blueprints
app.register_blueprint(admin_bp)

# Crear carpeta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==================== INICIALIZACIÓN ====================

@app.before_request
def before_request():
    """Configurar sesión permanente"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

@app.shell_context_processor
def make_shell_context():
    """Contexto para Flask shell"""
    return {
        'Servicio': Servicio,
        'Producto': Producto,
        'Cita': Cita,
        'Usuario': Usuario,
        'init_db': init_db
    }

# ==================== RUTAS PRINCIPALES ====================

@app.route("/")
def inicio():
    """Página de inicio"""
    servicios = Servicio.obtener_todos()
    productos = Producto.obtener_todos()[:6]  # Últimos 6 productos
    galerias = Galeria.obtener_todas()[:4]  # Últimas 4 galerías
    
    return render_template(
        "index.html",
        servicios=servicios,
        productos=productos,
        galerias=galerias
    )

@app.route("/servicios")
def servicios_pagina():
    """Página de servicios"""
    servicios = Servicio.obtener_todos()
    return render_template("servicios.html", servicios=servicios)

@app.route("/productos")
def tienda():
    """Página de tienda/productos"""
    categoria = request.args.get('categoria')
    
    if categoria:
        productos = Producto.obtener_por_categoria(categoria)
    else:
        productos = Producto.obtener_todos()
    
    categorias = list(set([p['categoria'] for p in Producto.obtener_todos()]))
    
    return render_template("tienda.html", productos=productos, categorias=categorias)

@app.route("/producto/<int:producto_id>")
def detalle_producto(producto_id):
    """Detalle de un producto"""
    producto = Producto.obtener_por_id(producto_id)
    
    if not producto:
        return render_template("404.html"), 404
    
    return render_template("producto_detalle.html", producto=producto)

@app.route("/galeria")
def galeria_pagina():
    """Página de galería antes/después"""
    galerias = Galeria.obtener_todas()
    return render_template("galeria.html", galerias=galerias)

@app.route("/contacto", methods=['GET', 'POST'])
def contacto():
    """Página de contacto"""
    if request.method == 'POST':
        data = request.get_json()
        
        try:
            Mensaje.crear(
                nombre=data['nombre'],
                email=data['email'],
                asunto=data['asunto'],
                mensaje=data['mensaje']
            )
            
            # Enviar email de confirmación
            enviar_email(
                data['email'],
                'Hemos recibido tu mensaje - Patitas Limpias',
                f"Hola {data['nombre']}, gracias por contactarnos."
            )
            
            return jsonify({'success': True, 'message': 'Mensaje enviado correctamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    return render_template("contacto.html")

# ==================== API DE CITAS ====================

@app.route("/api/citas/disponibles")
def citas_disponibles():
    """Obtener fechas y horas disponibles"""
    dias_adelante = int(request.args.get('dias', 14))
    fechas_disponibles = []
    
    for i in range(1, dias_adelante):
        fecha = datetime.now() + timedelta(days=i)
        # Saltar domingos
        if fecha.weekday() != 6:
            fechas_disponibles.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'dia': fecha.strftime('%A'),
                'display': fecha.strftime('%d/%m/%Y')
            })
    
    return jsonify(fechas_disponibles)

@app.route("/api/citas/horarios/<fecha>")
def citas_horarios(fecha):
    """Obtener horarios disponibles para una fecha"""
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        dia_semana = fecha_obj.strftime('%A')
        
        # Obtener horarios del día
        horarios = HorarioDisponible.obtener_por_dia(dia_semana)
        
        # Obtener citas ya reservadas para ese día
        citas_dia = Cita.obtener_por_fecha(fecha)
        horas_ocupadas = [c['hora_cita'] for c in citas_dia]
        
        horarios_disponibles = []
        for horario in horarios:
            inicio = datetime.strptime(horario['hora_inicio'], '%H:%M')
            fin = datetime.strptime(horario['hora_fin'], '%H:%M')
            intervalo = app.config['INTERVALO_CITAS']
            
            tiempo_actual = inicio
            while tiempo_actual < fin:
                hora_str = tiempo_actual.strftime('%H:%M')
                if hora_str not in horas_ocupadas:
                    horarios_disponibles.append(hora_str)
                tiempo_actual += timedelta(minutes=intervalo)
        
        return jsonify(horarios_disponibles)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/citas/agendar", methods=['POST'])
def agendar_cita():
    """Agendar una cita"""
    try:
        data = request.get_json()
        
        # Validar datos
        requeridos = ['nombre_cliente', 'email_cliente', 'telefono_cliente', 'nombre_mascota', 
                     'raza', 'fecha_cita', 'hora_cita', 'servicio_id']
        if not all(k in data for k in requeridos):
            return jsonify({'error': 'Faltan datos requeridos'}), 400
        
        # Crear cita
        cita_id = Cita.crear(
            nombre_cliente=data['nombre_cliente'],
            email_cliente=data['email_cliente'],
            telefono_cliente=data['telefono_cliente'],
            nombre_mascota=data['nombre_mascota'],
            raza=data['raza'],
            fecha_cita=data['fecha_cita'],
            hora_cita=data['hora_cita'],
            servicio_id=int(data['servicio_id']),
            notas=data.get('notas', '')
        )
        
        # Obtener detalles del servicio
        servicio = Servicio.obtener_por_id(int(data['servicio_id']))
        
        # Enviar confirmación por email
        enviar_email(
            data['email_cliente'],
            'Cita confirmada - Patitas Limpias',
            f"Tu cita para {data['nombre_mascota']} ha sido confirmada para el {data['fecha_cita']} a las {data['hora_cita']}"
        )
        
        # Enviar mensaje por WhatsApp
        mensaje_whatsapp = f"Hola {data['nombre_cliente']}, tu cita para {data['nombre_mascota']} ha sido confirmada. Fecha: {data['fecha_cita']} - Hora: {data['hora_cita']} - Servicio: {servicio['nombre']}"
        enviar_whatsapp(data['telefono_cliente'], mensaje_whatsapp)
        
        return jsonify({
            'success': True,
            'message': 'Cita agendada correctamente',
            'cita_id': cita_id
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== CARRITO ====================

@app.route("/api/carrito/agregar", methods=['POST'])
def agregar_carrito():
    """Agregar producto al carrito"""
    data = request.get_json()
    producto_id = data.get('producto_id')
    cantidad = int(data.get('cantidad', 1))
    
    producto = Producto.obtener_por_id(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    if not session.get('carrito'):
        session['carrito'] = []
    
    # Buscar si el producto ya está en el carrito
    item_existente = next((item for item in session['carrito'] if item['id'] == producto_id), None)
    
    if item_existente:
        item_existente['cantidad'] += cantidad
    else:
        session['carrito'].append({
            'id': producto_id,
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': cantidad,
            'imagen': producto['imagen']
        })
    
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': f'{producto["nombre"]} agregado al carrito',
        'carrito_items': len(session.get('carrito', []))
    })

@app.route("/carrito")
def carrito():
    """Ver carrito"""
    carrito_items = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    
    return render_template("carrito.html", carrito=carrito_items, total=total)

# ==================== AUTENTICACIÓN ====================

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login de usuario (opcional para clientes)"""
    if request.method == 'POST':
        data = request.get_json()
        # Aquí iría la lógica de login
        pass
    
    return render_template("login.html")

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    """Registro de usuario"""
    if request.method == 'POST':
        data = request.get_json()
        
        try:
            Usuario.crear(
                username=data['username'],
                email=data['email'],
                password=generate_password_hash(data['password']),
                nombre=data['nombre']
            )
            return jsonify({'success': True, 'message': 'Usuario registrado'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    return render_template("registro.html")

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def no_encontrado(error):
    """Página 404"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def error_servidor(error):
    """Página 500"""
    return render_template("500.html"), 500

@app.errorhandler(403)
def acceso_denegado(error):
    """Acceso denegado"""
    return render_template("403.html"), 403

# ==================== CONTEXTO GLOBAL ====================

@app.context_processor
def inject_config():
    """Inyectar configuración en todos los templates"""
    return {
        'ano_actual': datetime.now().year,
        'nombre_negocio': app.config['NOMBRE_NEGOCIO'],
        'email_negocio': app.config['EMAIL_NEGOCIO'],
        'telefono_negocio': app.config['TELEFONO_NEGOCIO'],
        'whatsapp_numero': app.config['WHATSAPP_NUMERO'],
        'carrito_items': len(session.get('carrito', []))
    }

# ==================== COMANDO DE INICIALIZACIÓN ====================

@app.cli.command()
def init_database():
    """Inicializar la base de datos"""
    init_db()
    print("✅ Base de datos inicializada")

@app.cli.command()
def create_admin():
    """Crear usuario administrador"""
    username = input("Usuario: ")
    email = input("Email: ")
    password = input("Contraseña: ")
    nombre = input("Nombre completo: ")
    
    Usuario.crear(
        username=username,
        email=email,
        password=generate_password_hash(password),
        nombre=nombre,
        es_admin=True
    )
    print(f"✅ Admin '{username}' creado exitosamente")

# ==================== EJECUTAR APLICACIÓN ====================

if __name__ == '__main__':
    # Inicializar base de datos si no existe
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            init_db()
            print("✅ Base de datos creada")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
        cita = {
            "id": len(citas_reservadas) + 1,
            "nombre_mascota": datos['nombre_mascota'],
            "raza": datos['raza'],
            "fecha": datos['fecha'],
            "hora": datos['hora'],
            "servicio": datos['servicio'],
            "fecha_registro": datetime.now().isoformat()
        }
        
        citas_reservadas.append(cita)
        
        return jsonify({
            "success": True,
            "mensaje": f"Cita agendada para {datos['nombre_mascota']}",
            "cita": cita
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/contacto", methods=["POST"])
def enviar_contacto():
    """API para enviar mensajes de contacto"""
    try:
        datos = request.get_json()
        
        # Validar datos
        if not all(k in datos for k in ('nombre', 'email', 'asunto', 'mensaje')):
            return jsonify({"error": "Faltan datos"}), 400
        
        # Guardar mensaje
        mensaje = {
            "id": len(mensajes_contacto) + 1,
            "nombre": datos['nombre'],
            "email": datos['email'],
            "asunto": datos['asunto'],
            "mensaje": datos['mensaje'],
            "fecha": datetime.now().isoformat(),
            "leido": False
        }
        
        mensajes_contacto.append(mensaje)
        
        return jsonify({
            "success": True,
            "mensaje": "Mensaje enviado correctamente",
            "id": mensaje['id']
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/citas")
def obtener_citas():
    """API para obtener todas las citas reservadas"""
    return jsonify(citas_reservadas)

@app.route("/api/mensajes")
def obtener_mensajes():
    """API para obtener todos los mensajes"""
    return jsonify(mensajes_contacto)

# MANEJO DE ERRORES
@app.errorhandler(404)
def no_encontrado(error):
    """Página 404"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def error_servidor(error):
    """Página de error 500"""
    return render_template("500.html"), 500

# CONTEXTO PARA TEMPLATES
@app.context_processor
def inject_config():
    return {
        'ano_actual': datetime.now().year,
        'nombre_negocio': 'Patitas Limpias',
        'email': 'info@patilaslimpias.com',
        'telefono': '+34 123 456 789'
    }

# EJECUTAR APLICACIÓN
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
    

if __name__ == "__main__":
    app.run(debug=True)