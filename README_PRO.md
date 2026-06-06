# 🐾 Patitas Limpias - Peluquería y PetShop Canino

Plataforma web profesional para una peluquería y petshop canino con sistema de citas, catálogo dinámico y panel administrativo.

## ✨ Características

### Frontend
- 🎨 Diseño responsivo moderno con Bootstrap 5
- 📱 Interfaz amigable para móvil, tablet y desktop
- 🛒 Carrito de compras funcional
- 📅 Sistema de agendamiento de citas
- 🖼️ Galería antes/después
- 💬 Formulario de contacto
- 🔗 Integración con WhatsApp

### Backend
- 🔐 Sistema de autenticación seguro
- 🗄️ Base de datos SQLite
- 👨‍💼 Panel administrativo completo
- 📊 Dashboard con estadísticas
- 📧 Notificaciones por email
- 💬 Integración con WhatsApp
- 📸 Carga de imágenes para productos y galería
- 📋 Sistema de citas con horarios disponibles

### Panel Administrativo
- 📅 Gestión de citas y horarios
- 🛍️ Administración de productos y categorías
- ✂️ Gestión de servicios
- 🖼️ Galería antes/después
- 💌 Gestión de mensajes
- 📊 Reportes y estadísticas

## 🚀 Instalación

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/gittrabajo/Peluqueria-y-PetShop-Canina-PatitasLimpias.git
cd PatitasLimpiasWeb
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
- En Windows:
```bash
venv\Scripts\activate
```
- En macOS/Linux:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Inicializar la base de datos**
```bash
flask init-database
```

6. **Crear usuario administrador**
```bash
flask create-admin
```

7. **Ejecutar la aplicación**
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
PatitasLimpiasWeb/
├── app.py                 # Aplicación principal
├── config.py              # Configuración
├── database.py            # Inicialización de base de datos
├── models.py              # Modelos de datos
├── routes_admin.py        # Rutas administrativas
├── utils.py               # Funciones auxiliares
├── requirements.txt       # Dependencias
├── templates/
│   ├── index.html
│   ├── servicios.html
│   ├── tienda.html
│   ├── contacto.html
│   ├── carrito.html
│   ├── galeria.html
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── productos.html
│       ├── citas.html
│       ├── servicios.html
│       ├── galeria.html
│       ├── mensajes.html
│       └── reportes.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── uploads/           # Carpeta para imágenes subidas
├── database/              # Archivo de base de datos
└── models/                # Modelos de datos

```

## 🔐 Credenciales por Defecto

Después de crear un administrador, usa tus credenciales para acceder al panel:
- URL: `http://localhost:5000/admin/login`

## 🎯 Funcionalidades Principales

### Para Clientes
1. **Página de Inicio** - Showcasing de servicios y productos
2. **Agendar Citas** - Sistema de reservas con horarios disponibles
3. **Tienda Online** - Catálogo de productos con carrito
4. **Galería** - Fotos antes/después de trabajos
5. **Contacto** - Formulario de contacto y WhatsApp

### Para Administradores
1. **Dashboard** - Vista general del negocio
2. **Gestión de Citas** - Ver, editar y cancelar citas
3. **Gestión de Servicios** - Agregar, editar, eliminar servicios
4. **Gestión de Productos** - Administrar inventario
5. **Galería** - Agregar fotos antes/después
6. **Mensajes** - Responder consultas
7. **Reportes** - Estadísticas del negocio

## 🔗 Integración con WhatsApp

Para habilitar WhatsApp automático:
1. Editar `config.py` - Actualizar `WHATSAPP_NUMERO`
2. Integrar con API de WhatsApp Business (Twilio, Meta)

## 📧 Configuración de Email

Para notificaciones por email:
1. Instalar Flask-Mail: `pip install Flask-Mail`
2. Configurar credenciales en `config.py`

## 🛠️ Comandos Útiles

```bash
# Inicializar base de datos
flask init-database

# Crear usuario admin
flask create-admin

# Ejecutar en modo debug
python app.py

# Ejecutar con Gunicorn (producción)
gunicorn app:app
```

## 📱 APIs Disponibles

### Citas
- `GET /api/citas/disponibles` - Fechas disponibles
- `GET /api/citas/horarios/<fecha>` - Horarios para una fecha
- `POST /api/citas/agendar` - Agendar cita

### Carrito
- `POST /api/carrito/agregar` - Agregar producto al carrito

### Admin
- `POST /admin/api/servicios` - Crear servicio
- `POST /admin/api/productos` - Crear producto
- `PUT /admin/api/citas/<id>/estado` - Actualizar estado de cita

## 🚀 Despliegue en Producción

### Opción 1: Heroku
```bash
heroku create patitas-limpias
git push heroku main
```

### Opción 2: AWS
1. Crear instancia EC2
2. Instalar Python y dependencias
3. Usar Gunicorn + Nginx

### Opción 3: DigitalOcean
1. Crear droplet Ubuntu
2. Instalar Python
3. Configurar Gunicorn + Nginx

## 📞 Contacto y Soporte

- Email: info@patilaslimpias.com
- WhatsApp: +34 123 456 789
- GitHub: https://github.com/gittrabajo/Peluqueria-y-PetShop-Canina-PatitasLimpias

## 📄 Licencia

Este proyecto es de código abierto bajo licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crear rama con tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

Hecho con ❤️ para Patitas Limpias
