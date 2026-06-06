from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os

# Importar configuración
from config import DevelopmentConfig
from database import init_db
from models import Servicio, Producto, Cita, Mensaje, Usuario, HorarioDisponible, Galeria

# NOTA: Los modelos ORM (Reserva, Producto con SQLAlchemy) están en models/ 
# pero no se importan aquí para evitar conflictos con models.py
# Se pueden usar cuando se implemente SQLAlchemy en el futuro

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

# Alias para facilitar URL
@app.route("/tienda")
def tienda_alias():
    """Alias de /productos"""
    return tienda()

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
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            email = request.form.get('email')
            asunto = request.form.get('asunto')
            mensaje = request.form.get('mensaje')
            
            # Crear mensaje
            Mensaje.crear(
                nombre=nombre,
                email=email,
                asunto=asunto,
                mensaje=mensaje
            )
            
            # Enviar email de confirmación
            enviar_email(
                email,
                'Hemos recibido tu mensaje - Patitas Limpias',
                f"Hola {nombre}, gracias por contactarnos. Pronto nos comunicaremos contigo."
            )
            
            # Redirigir con mensaje de éxito
            return render_template("contacto.html", success=True, message="¡Mensaje enviado correctamente! Pronto nos comunicaremos contigo.")
        except Exception as e:
            print(f"Error al enviar contacto: {str(e)}")
            return render_template("contacto.html", error=True, message=f"Error al enviar el mensaje: {str(e)}")
    
    return render_template("contacto.html")

# ==================== RESERVAS DE SERVICIOS ====================

@app.route("/agenda")
def agenda():
    """
    Página para reservar servicios (citas de grooming)
    Muestra servicios disponibles y botón de WhatsApp
    """
    whatsapp_numero = app.config.get('WHATSAPP_NUMERO', '34123456789')
    return render_template("agenda.html", whatsapp_numero=whatsapp_numero)

@app.route("/reservar", methods=['POST'])
def reservar():
    """
    Procesar nueva reserva de servicio
    Parámetros POST: cliente, mascota, servicio, fecha, hora
    """
    try:
        # Obtener datos del formulario
        cliente = request.form.get('cliente')
        mascota = request.form.get('mascota')
        servicio = request.form.get('servicio')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        notas = request.form.get('notas', '')
        
        # Validar datos requeridos
        if not all([cliente, mascota, servicio, fecha, hora]):
            return redirect(url_for('agenda')), {
                'error': 'Todos los campos son requeridos'
            }
        
        # Crear la reserva
        nueva_reserva = Reserva(
            cliente=cliente,
            mascota=mascota,
            servicio=servicio,
            fecha=fecha,
            hora=hora,
            notas=notas,
            estado='Pendiente'
        )
        
        # Guardar en base de datos (si está disponible)
        # db.session.add(nueva_reserva)
        # db.session.commit()
        
        # Mostrar mensaje de éxito
        print(f"✅ Reserva creada: {cliente} - {mascota} - {servicio}")
        
        return redirect(url_for('inicio'))
    
    except Exception as e:
        print(f"❌ Error al crear reserva: {str(e)}")
        return redirect(url_for('agenda'))

# ==================== PANEL DE ADMINISTRADOR ====================

@app.route("/admin")
def admin():
    """
    Panel de administración
    Permite gestionar productos y reservas
    """
    from models import Producto
    productos = Producto.obtener_todos()
    return render_template("admin.html", productos=productos)

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

# ==================== CARRITO DE COMPRAS ====================
# Sistema completo de carrito con almacenamiento en localStorage (frontend)
# Las rutas API aquí son opcionales para sincronización con servidor

@app.route("/carrito")
def carrito():
    """Página del carrito (puede ser usada para checkout futuro)"""
    carrito_items = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    
    return render_template("carrito.html", carrito=carrito_items, total=total)

@app.route("/api/carrito/info", methods=['GET'])
def obtener_info_carrito():
    """
    Obtener información del carrito almacenado en servidor
    (Respaldo de información del carrito del cliente)
    """
    carrito_items = session.get('carrito', [])
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    impuesto = subtotal * 0.16  # IVA 16%
    total = subtotal + impuesto
    
    return jsonify({
        'success': True,
        'items': carrito_items,
        'cantidad_items': len(carrito_items),
        'cantidad_total': sum(item['cantidad'] for item in carrito_items),
        'subtotal': round(subtotal, 2),
        'impuesto': round(impuesto, 2),
        'total': round(total, 2)
    })

@app.route("/api/carrito/agregar", methods=['POST'])
def api_agregar_carrito():
    """
    API para agregar producto al carrito (almacenado en servidor)
    El carrito principal se maneja con localStorage en el frontend
    """
    data = request.get_json()
    producto_id = data.get('producto_id')
    cantidad = int(data.get('cantidad', 1))
    
    # Buscar el producto
    producto = Producto.obtener_por_id(producto_id)
    if not producto:
        return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
    
    # Validar cantidad
    if cantidad <= 0:
        return jsonify({'success': False, 'error': 'Cantidad debe ser mayor a 0'}), 400
    
    # Validar stock disponible
    if producto['stock'] < cantidad:
        return jsonify({
            'success': False, 
            'error': f'Stock insuficiente. Disponible: {producto["stock"]}'
        }), 400
    
    # Inicializar carrito en sesión si no existe
    if not session.get('carrito'):
        session['carrito'] = []
    
    # Buscar si el producto ya está en el carrito
    item_existente = next((item for item in session['carrito'] if item['id'] == producto_id), None)
    
    if item_existente:
        # Aumentar cantidad si ya existe
        nueva_cantidad = item_existente['cantidad'] + cantidad
        if producto['stock'] < nueva_cantidad:
            return jsonify({
                'success': False,
                'error': f'Stock insuficiente. Disponible: {producto["stock"]}'
            }), 400
        item_existente['cantidad'] = nueva_cantidad
    else:
        # Agregar nuevo producto al carrito
        session['carrito'].append({
            'id': producto_id,
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': cantidad,
            'imagen': producto.get('imagen', 'static/img/default-product.jpg')
        })
    
    # Marcar sesión como modificada
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': f'✓ {producto["nombre"]} agregado al carrito',
        'cantidad_carrito': len(session.get('carrito', []))
    }), 201

@app.route("/api/carrito/limpiar", methods=['POST'])
def limpiar_carrito():
    """Vaciar completamente el carrito"""
    session['carrito'] = []
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': 'Carrito vaciado'
    })

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