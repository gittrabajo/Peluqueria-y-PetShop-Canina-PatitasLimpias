from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Variables globales (en un proyecto real usarías una base de datos)
citas_reservadas = []
mensajes_contacto = []

# RUTAS PRINCIPALES
@app.route("/")
def inicio():
    """Página de inicio"""
    return render_template("index.html")

@app.route("/servicios")
def servicios():
    """Página de servicios"""
    servicios_data = [
        {"id": 1, "nombre": "Corte de Pelo", "precio": 30, "descripcion": "Cortes profesionales adaptados a la raza"},
        {"id": 2, "nombre": "Baño y Secado", "precio": 25, "descripcion": "Baño relajante con productos premium"},
        {"id": 3, "nombre": "Tratamientos", "precio": 40, "descripcion": "Tratamientos especiales para la piel"},
        {"id": 4, "nombre": "SPA Canino", "precio": 75, "descripcion": "Experiencia SPA completa"},
    ]
    return jsonify(servicios_data)

@app.route("/productos")
def productos():
    """Página de productos"""
    productos_data = [
        {"id": 1, "nombre": "Champú Premium", "precio": 25.99, "categoria": "Cuidado"},
        {"id": 2, "nombre": "Acondicionador", "precio": 22.99, "categoria": "Cuidado"},
        {"id": 3, "nombre": "Kit de Aseo", "precio": 45.99, "categoria": "Kits"},
    ]
    return jsonify(productos_data)

# RUTAS DE FUNCIONALIDAD
@app.route("/api/agendar", methods=["POST"])
def agendar_cita():
    """API para agendar citas"""
    try:
        datos = request.get_json()
        
        # Validar datos
        if not all(k in datos for k in ('nombre_mascota', 'raza', 'fecha', 'hora', 'servicio')):
            return jsonify({"error": "Faltan datos"}), 400
        
        # Guardar cita
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
    )

if __name__ == "__main__":
    app.run(debug=True)