from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from utils import admin_required, login_required, save_upload_file
from models import Usuario, Servicio, Producto, Cita, HorarioDisponible, Galeria, Mensaje
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ==================== AUTENTICACIÓN ====================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login del administrador"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        usuario = Usuario.obtener_por_username(username)
        
        if usuario and check_password_hash(usuario['password'], password) and usuario['es_admin']:
            session['user_id'] = usuario['id']
            session['username'] = usuario['username']
            session['es_admin'] = usuario['es_admin']
            return jsonify({'success': True, 'redirect': url_for('admin.dashboard')})
        else:
            return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Logout del administrador"""
    session.clear()
    return redirect(url_for('admin.login'))

# ==================== DASHBOARD ====================

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Panel de control principal"""
    # Estadísticas
    citas = Cita.obtener_todas()
    productos = Producto.obtener_todos()
    mensajes = Mensaje.obtener_todos()
    
    # Contar no leídos
    mensajes_no_leidos = sum(1 for m in mensajes if not m['leido'])
    
    # Citas de hoy
    hoy = datetime.now().strftime('%Y-%m-%d')
    citas_hoy = Cita.obtener_por_fecha(hoy)
    
    stats = {
        'total_citas': len(citas),
        'citas_hoy': len(citas_hoy),
        'total_productos': len(productos),
        'productos_bajo_stock': sum(1 for p in productos if p['stock'] < 5),
        'mensajes_nuevos': mensajes_no_leidos
    }
    
    return render_template('admin/dashboard.html', stats=stats, citas_hoy=citas_hoy)

# ==================== SERVICIOS ====================

@admin_bp.route('/servicios')
@admin_required
def servicios():
    """Gestionar servicios"""
    servicios = Servicio.obtener_todos()
    return render_template('admin/servicios.html', servicios=servicios)

@admin_bp.route('/api/servicios', methods=['POST'])
@admin_required
def crear_servicio():
    """Crear nuevo servicio"""
    data = request.get_json()
    
    try:
        Servicio.crear(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio=float(data['precio']),
            duracion_minutos=int(data.get('duracion_minutos', 60))
        )
        return jsonify({'success': True, 'message': 'Servicio creado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== PRODUCTOS ====================

@admin_bp.route('/productos')
@admin_required
def productos():
    """Gestionar productos"""
    productos = Producto.obtener_todos()
    return render_template('admin/productos.html', productos=productos)

@admin_bp.route('/api/productos', methods=['POST'])
@admin_required
def crear_producto():
    """Crear nuevo producto"""
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio'))
        categoria = request.form.get('categoria')
        stock = int(request.form.get('stock', 0))
        
        imagen_url = None
        if 'imagen' in request.files:
            imagen_url = save_upload_file(request.files['imagen'])
        
        Producto.crear(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria,
            stock=stock,
            imagen=imagen_url
        )
        
        return jsonify({'success': True, 'message': 'Producto creado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== CITAS ====================

@admin_bp.route('/citas')
@admin_required
def citas():
    """Gestionar citas"""
    citas = Cita.obtener_todas()
    return render_template('admin/citas.html', citas=citas)

@admin_bp.route('/api/citas/<int:cita_id>/estado', methods=['PUT'])
@admin_required
def actualizar_estado_cita(cita_id):
    """Actualizar estado de una cita"""
    data = request.get_json()
    nuevo_estado = data.get('estado')
    
    if nuevo_estado not in ['confirmada', 'cancelada', 'completada']:
        return jsonify({'success': False, 'error': 'Estado inválido'}), 400
    
    try:
        Cita.actualizar_estado(cita_id, nuevo_estado)
        return jsonify({'success': True, 'message': 'Estado actualizado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== HORARIOS ====================

@admin_bp.route('/horarios')
@admin_required
def horarios():
    """Gestionar horarios disponibles"""
    horarios = HorarioDisponible.obtener_todos()
    return render_template('admin/horarios.html', horarios=horarios)

@admin_bp.route('/api/horarios', methods=['POST'])
@admin_required
def crear_horario():
    """Crear nuevo horario"""
    data = request.get_json()
    
    try:
        HorarioDisponible.crear(
            dia_semana=data['dia_semana'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin']
        )
        return jsonify({'success': True, 'message': 'Horario creado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== GALERÍA ====================

@admin_bp.route('/galeria')
@admin_required
def galeria():
    """Gestionar galería antes/después"""
    galerias = Galeria.obtener_todas()
    return render_template('admin/galeria.html', galerias=galerias)

@admin_bp.route('/api/galeria', methods=['POST'])
@admin_required
def crear_galeria():
    """Crear entrada de galería"""
    try:
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        
        imagen_antes_url = None
        imagen_despues_url = None
        
        if 'imagen_antes' in request.files:
            imagen_antes_url = save_upload_file(request.files['imagen_antes'])
        
        if 'imagen_despues' in request.files:
            imagen_despues_url = save_upload_file(request.files['imagen_despues'])
        
        Galeria.crear(
            titulo=titulo,
            imagen_antes=imagen_antes_url,
            imagen_despues=imagen_despues_url,
            descripcion=descripcion
        )
        
        return jsonify({'success': True, 'message': 'Galería creada'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== MENSAJES ====================

@admin_bp.route('/mensajes')
@admin_required
def mensajes():
    """Ver mensajes de contacto"""
    mensajes = Mensaje.obtener_todos()
    return render_template('admin/mensajes.html', mensajes=mensajes)

@admin_bp.route('/api/mensajes/<int:mensaje_id>/leido', methods=['PUT'])
@admin_required
def marcar_mensaje_leido(mensaje_id):
    """Marcar mensaje como leído"""
    try:
        Mensaje.marcar_leido(mensaje_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== REPORTES ====================

@admin_bp.route('/reportes')
@admin_required
def reportes():
    """Ver reportes y estadísticas"""
    citas = Cita.obtener_todas()
    productos = Producto.obtener_todos()
    
    # Calcular estadísticas
    total_citas = len(citas)
    citas_completadas = sum(1 for c in citas if c['estado'] == 'completada')
    
    productos_bajo_stock = [p for p in productos if p['stock'] < 5]
    
    stats = {
        'total_citas': total_citas,
        'citas_completadas': citas_completadas,
        'tasa_completacion': f"{(citas_completadas/total_citas*100) if total_citas > 0 else 0:.1f}%",
        'productos_bajo_stock': len(productos_bajo_stock),
        'total_productos': len(productos)
    }
    
    return render_template('admin/reportes.html', stats=stats, productos_bajo_stock=productos_bajo_stock)
