import os
from datetime import timedelta

class Config:
    """Configuración base"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'patitas-limpias-secret-key-2024'
    DEBUG = False
    TESTING = False
    
    # Sesión
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Cargas de archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    
    # Base de datos
    DATABASE = 'patitas_limpias.db'
    
    # Negocio
    NOMBRE_NEGOCIO = 'Patitas Limpias'
    EMAIL_NEGOCIO = 'info@patilaslimpias.com'
    TELEFONO_NEGOCIO = '+34 123 456 789'
    WHATSAPP_NUMERO = '34123456789'
    
    # Horarios de atención (formato 24h)
    HORARIOS_ATENCION = {
        'Lunes': {'inicio': '09:00', 'fin': '18:00'},
        'Martes': {'inicio': '09:00', 'fin': '18:00'},
        'Miércoles': {'inicio': '09:00', 'fin': '18:00'},
        'Jueves': {'inicio': '09:00', 'fin': '18:00'},
        'Viernes': {'inicio': '09:00', 'fin': '18:00'},
        'Sábado': {'inicio': '10:00', 'fin': '14:00'},
        'Domingo': {'inicio': 'CERRADO', 'fin': 'CERRADO'},
    }
    
    # Intervalo mínimo entre citas (en minutos)
    INTERVALO_CITAS = 30

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Configuración de pruebas"""
    TESTING = True
    DEBUG = True
    DATABASE = ':memory:'

# Selector de configuración
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
