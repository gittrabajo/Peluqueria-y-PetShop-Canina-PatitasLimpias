# GUÍA RÁPIDA - PATITAS LIMPIAS

## 🚀 INICIO RÁPIDO

### Ejecutar la aplicación:
```bash
python app.py
```

Luego abre: `http://localhost:5000`

---

## 📖 NAVEGACIÓN PRINCIPAL

### 1. **Página de Inicio** (`/`)
- Muestra servicios destacados
- Últimos productos
- Galería de fotos
- Enlaces de navegación

### 2. **Tienda** (`/tienda` o `/productos`)
- Catálogo de productos
- Filtros por categoría
- Búsqueda por nombre
- Ordenamiento
- **Carrito integrado** ⭐

### 3. **Reservar Servicio** (`/agenda`)
- Seleccionar servicio:
  - 🚿 Baño (45 min)
  - 💇 Baño y Corte (90 min)
  - 💨 Deslanado (60 min)
  - 💄 Peluquería Completa (120 min)
- Completar formulario
- Confirmar reserva

### 4. **Panel Admin** (`/admin`)
- 📊 Resumen de estadísticas
- 📦 Gestión de productos
- 📅 Gestión de reservas
- ⚙️ Configuración del sistema

### 5. **Contacto** (`/contacto`)
- Enviar mensaje
- Información de contacto
- Horarios de atención

---

## 🛒 GUÍA DEL CARRITO

### 🔴 Agregar Producto al Carrito

1. Ve a `/tienda`
2. Haz click en **"Agregar al Carrito"** (botón verde)
3. Verás feedback visual ✅
4. El contador en navbar se actualiza

### 🛍️ Abrir el Carrito

- Click en icono de **carrito** en la navbar
- O presiona el badge con el número
- Se abre un sidebar desde la derecha

### 📝 Modificar Cantidad

En el carrito abierto:
- **Botón -**: Disminuir cantidad
- **Input**: Ingresar cantidad directa
- **Botón +**: Aumentar cantidad

### ❌ Eliminar Producto

- Click en el icono de **papelera** roja
- Producto se elimina inmediatamente

### 💰 Ver Totales

El carrito muestra:
- **Subtotal**: Suma de precios × cantidad
- **IVA (16%)**: Impuesto automático
- **Total**: Lo que debes pagar

### 🛑 Vaciar Carrito

1. Abre el carrito
2. Limpiar manualmente o
3. Click en "Limpiar" (en casos específicos)

### ✅ Comprar

1. Click en botón **"Comprar"**
2. Confirma el total
3. ¡Listo! Compra procesada

### 💾 Persistencia

El carrito se guarda automáticamente:
- Se conserva al recargar la página
- Se conserva al cerrar el navegador
- Se mantiene entre sesiones

---

## 📊 PRODUCTOS DISPONIBLES

### Ejemplo de Productos en Tienda:

1. **Champú Premium Hipoalergénico** - $24.99
   - Categoría: Champús
   - Descripción: Para pieles sensibles

2. **Alimento Premium para Perros** - $34.99
   - Categoría: Alimentos
   - Descripción: Bolsa 5kg, proteínas de calidad

3. **Juguete Interactivo Inteligente** - $19.99
   - Categoría: Juguetes
   - Descripción: Estimula inteligencia canina

4. **Collar Premium con GPS** - $89.99
   - Categoría: Accesorios
   - Descripción: Localiza a tu mascota en tiempo real

---

## 🛠️ CARACTERÍSTICAS TÉCNICAS DEL CARRITO

### Almacenamiento
- ✅ localStorage del navegador
- ✅ Datos persisten automáticamente
- ✅ No requiere servidor
- ✅ Rápido y seguro

### Cálculos Automáticos
- ✅ Subtotal = Precio × Cantidad
- ✅ IVA = Subtotal × 16%
- ✅ Total = Subtotal + IVA
- ✅ Actualización en tiempo real

### Validaciones
- ✅ Stock disponible verificado
- ✅ Cantidad mínima (1 item)
- ✅ Confirmación antes de limpiar
- ✅ Mensajes de error claros

### Interfaz Responsive
- ✅ Desktop: Sidebar 400px a la derecha
- ✅ Tablet: Se adapta al ancho
- ✅ Móvil: Fullscreen (100% ancho)
- ✅ Overlay para cerrar fácil

---

## 🔍 DEBUGGING DEL CARRITO

### En la Consola del Navegador (F12):

```javascript
// Ver carrito actual
debugCarrito()

// Agregar producto de prueba
agregarAlCarrito({
  id: 99,
  nombre: "Producto Prueba",
  precio: 50,
  cantidad: 1,
  imagen: "static/img/default.jpg"
})

// Ver cantidad total
obtenerCantidadTotal()

// Ver total a pagar
calcularTotal()

// Vaciar carrito
vaciarCarrito()

// Abrir carrito
abrirCarrito()

// Cerrar carrito
cerrarCarrito()
```

---

## 📱 RESPONSIVE

### Desktop (>768px)
- Navbar completa
- Sidebar carrito: 400px
- 4 columnas de productos

### Tablet (768px - 1024px)
- Navbar responsive
- Sidebar carrito: ancho completo
- 2-3 columnas de productos

### Móvil (<768px)
- Navbar hamburguesa
- Sidebar carrito: fullscreen
- 1-2 columnas de productos

---

## ⌨️ ATAJOS

### Teclado
- Tab: Navegar entre elementos
- Enter: Confirmar
- Escape: Cerrar carrito
- Space: Activar botones

### Ratón
- Click: Acciones
- Hover: Ver efectos visuales
- Scroll: Navegar página

---

## 🎨 COLORES

| Elemento | Color | Código |
|----------|-------|--------|
| Primary | Morado claro | #667eea |
| Secondary | Morado oscuro | #764ba2 |
| Success | Verde | #28a745 |
| Warning | Amarillo | #ffc107 |
| Danger | Rojo | #dc3545 |
| Light | Gris claro | #f8f9fa |

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Carrito no se abre
- Verifica que JavaScript esté habilitado
- Recarga la página (F5)
- Abre DevTools y ve si hay errores

### Carrito no guarda datos
- Verifica localStorage en DevTools
- Intenta con modo incógnito
- Limpia cookies/cache del navegador

### Producto no agrega
- Verifica que el producto tenga ID
- Comprueba que hay stock disponible
- Revisa la consola de errores (F12)

### Precios no se calculan
- Recarga la página
- Limpia el carrito y agrega de nuevo
- Verifica que los precios sean números

---

## 📞 CONTACTO Y SOPORTE

**Email**: info@patilaslimpias.com
**Teléfono**: +34 123 456 789
**WhatsApp**: +34 123 456 789
**Horario**: Lunes-Viernes 9:00-18:00 | Sábado 10:00-14:00

---

## ✨ TIPS Y TRUCOS

1. **Buscar rápido**: Usa el filtro de búsqueda en tienda
2. **Ordenar**: Selecciona orden por precio o nombre
3. **Favoritos**: Click en corazón (próximamente)
4. **Mobile First**: Prueba en móvil primero
5. **Debug**: Abre DevTools con F12
6. **Hotkeys**: Usa Tab para navegar sin ratón

---

**¡Disfruta usando Patitas Limpias!** 🐾
