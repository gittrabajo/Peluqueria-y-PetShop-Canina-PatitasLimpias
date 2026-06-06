import os
import requests
from werkzeug.utils import secure_filename
from config import Config
from functools import wraps
from flask import session, redirect, url_for, abort

def allowed_file(filename):
    """Validar si el archivo es permitido"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_upload_file(file):
    """Guardar archivo subido"""
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Agregar timestamp para evitar conflictos
        import time
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return f"/static/uploads/{filename}"
    return None

def enviar_whatsapp(numero, mensaje):
    """Enviar mensaje por WhatsApp"""
    try:
        # Usando Twilio o WhatsApp Business API
        # Para desarrollo, simplemente retornar True
        # En producción, integrar con el servicio real
        
        # Ejemplo con URL de WhatsApp Web
        url = f"https://wa.me/{numero}?text={requests.utils.quote(mensaje)}"
        return {'success': True, 'url': url}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def enviar_email(destinatario, asunto, cuerpo):
    """Enviar email (implementar con Flask-Mail en producción)"""
    try:
        # Para desarrollo, simular envío
        print(f"📧 Email enviado a {destinatario}")
        print(f"Asunto: {asunto}")
        print(f"Cuerpo: {cuerpo}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        return False

def login_required(f):
    """Decorador para requerir login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir acceso de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if not session.get('es_admin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def generar_numero_pedido():
    """Generar número único de pedido"""
    from datetime import datetime
    import random
    fecha = datetime.now().strftime('%Y%m%d')
    numero_aleatorio = random.randint(1000, 9999)
    return f"PL-{fecha}-{numero_aleatorio}"

def calcular_precio_total(items_carrito):
    """Calcular precio total del carrito"""
    total = 0
    for item in items_carrito:
        total += item['precio'] * item['cantidad']
    return round(total, 2)

def generar_plantilla_email_cita(nombre_cliente, nombre_mascota, fecha, hora, servicio):
    """Generar plantilla de email para confirmación de cita"""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #667eea;">✅ Cita Confirmada - Patitas Limpias</h2>
                
                <p>Hola <strong>{nombre_cliente}</strong>,</p>
                
                <p>Tu cita ha sido confirmada exitosamente. Aquí están los detalles:</p>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0;">
                    <p><strong>🐕 Mascota:</strong> {nombre_mascota}</p>
                    <p><strong>📅 Fecha:</strong> {fecha}</p>
                    <p><strong>⏰ Hora:</strong> {hora}</p>
                    <p><strong>💅 Servicio:</strong> {servicio}</p>
                </div>
                
                <p>Si necesitas cancelar o reprogramar, por favor contactanos con anticipación.</p>
                
                <p style="margin-top: 30px; text-align: center;">
                    <a href="https://wa.me/{Config.WHATSAPP_NUMERO}" 
                       style="background-color: #25d366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Contactar por WhatsApp
                    </a>
                </p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                
                <p style="color: #666; font-size: 12px;">
                    © 2024 Patitas Limpias. Todos los derechos reservados.
                </p>
            </div>
        </body>
    </html>
    """

def generar_plantilla_email_contacto(nombre, asunto, mensaje):
    """Generar plantilla de email para confirmación de contacto"""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Hola {nombre},</h2>
            <p>Hemos recibido tu mensaje. Nos pondremos en contacto contigo pronto.</p>
            
            <h3>Resumen de tu mensaje:</h3>
            <p><strong>Asunto:</strong> {asunto}</p>
            <p><strong>Mensaje:</strong> {mensaje}</p>
            
            <p>Gracias por contactarnos.</p>
            <p>Patitas Limpias</p>
        </body>
    </html>
    """
