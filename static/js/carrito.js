// ====================================================
// SISTEMA DE CARRITO DE COMPRAS - carrito.js
// ====================================================
// Este archivo maneja toda la lógica del carrito interactivo
// Incluye: agregar, quitar, actualizar cantidad, cálculo de total

// ========== VARIABLES GLOBALES ==========

// Carrito almacenado en localStorage
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Constantes
const STORAGE_KEY = 'carrito';
const TAX_PERCENTAGE = 0.16; // IVA 16%


// ========== INICIALIZACIÓN ==========

/**
 * Se ejecuta cuando el DOM está completamente cargado
 * Inicializa los listeners y actualiza la vista del carrito
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛒 Sistema de carrito inicializado');
    
    // Actualizar contador y vista del carrito
    actualizarCarrito();
    
    // Listeners para botones del carrito
    configurarListeners();
});


// ========== FUNCIONES PRINCIPALES DE CARRITO ==========

/**
 * Agregar un producto al carrito
 * @param {Object} producto - Objeto con datos del producto
 * @param {number} producto.id - ID único del producto
 * @param {string} producto.nombre - Nombre del producto
 * @param {number} producto.precio - Precio unitario
 * @param {number} producto.cantidad - Cantidad (por defecto 1)
 * @param {string} producto.imagen - URL de la imagen
 */
function agregarAlCarrito(producto) {
    console.log('➕ Agregando al carrito:', producto.nombre);
    
    // Verificar si el producto ya existe en el carrito
    const productoExistente = carrito.find(p => p.id == producto.id);
    
    if (productoExistente) {
        // Si ya existe, aumentar cantidad
        productoExistente.cantidad += (producto.cantidad || 1);
        console.log(`📦 ${producto.nombre} - Cantidad ahora: ${productoExistente.cantidad}`);
    } else {
        // Si no existe, agregarlo al carrito
        carrito.push({
            id: producto.id,
            nombre: producto.nombre,
            precio: producto.precio,
            cantidad: producto.cantidad || 1,
            imagen: producto.imagen || 'static/img/default-product.jpg'
        });
        console.log(`✨ ${producto.nombre} agregado al carrito`);
    }
    
    // Guardar en localStorage y actualizar vista
    guardarCarrito();
    actualizarCarrito();
    
    // Abrir carrito automáticamente (opcional)
    abrirCarrito();
}

/**
 * Eliminar un producto del carrito
 * @param {number} productoId - ID del producto a eliminar
 */
function eliminarDelCarrito(productoId) {
    console.log('❌ Eliminando del carrito:', productoId);
    
    carrito = carrito.filter(p => p.id != productoId);
    guardarCarrito();
    actualizarCarrito();
}

/**
 * Actualizar la cantidad de un producto
 * @param {number} productoId - ID del producto
 * @param {number} nuevaCantidad - Nueva cantidad
 */
function actualizarCantidad(productoId, nuevaCantidad) {
    console.log(`🔄 Actualizando ${productoId} a cantidad ${nuevaCantidad}`);
    
    const producto = carrito.find(p => p.id == productoId);
    
    if (producto) {
        if (nuevaCantidad <= 0) {
            eliminarDelCarrito(productoId);
        } else {
            producto.cantidad = parseInt(nuevaCantidad);
            guardarCarrito();
            actualizarCarrito();
        }
    }
}

/**
 * Vaciar completamente el carrito
 */
function vaciarCarrito() {
    if (confirm('¿Estás seguro de que deseas vaciar el carrito?')) {
        console.log('🗑️ Vaciando carrito...');
        carrito = [];
        guardarCarrito();
        actualizarCarrito();
    }
}


// ========== FUNCIONES DE ALMACENAMIENTO ==========

/**
 * Guardar carrito en localStorage
 */
function guardarCarrito() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(carrito));
    console.log('💾 Carrito guardado en localStorage');
}

/**
 * Obtener carrito desde localStorage
 */
function obtenerCarrito() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
}


// ========== FUNCIONES DE CÁLCULO ==========

/**
 * Calcular subtotal del carrito
 * @returns {number} Subtotal sin impuestos
 */
function calcularSubtotal() {
    return carrito.reduce((total, producto) => {
        return total + (producto.precio * producto.cantidad);
    }, 0);
}

/**
 * Calcular impuesto (IVA)
 * @returns {number} Monto del impuesto
 */
function calcularImpuesto() {
    return calcularSubtotal() * TAX_PERCENTAGE;
}

/**
 * Calcular total del carrito
 * @returns {number} Total a pagar
 */
function calcularTotal() {
    return calcularSubtotal() + calcularImpuesto();
}

/**
 * Obtener cantidad total de items en el carrito
 * @returns {number} Cantidad de items
 */
function obtenerCantidadTotal() {
    return carrito.reduce((total, producto) => total + producto.cantidad, 0);
}


// ========== FUNCIONES DE ACTUALIZACIÓN DE VISTA ==========

/**
 * Actualizar la vista completa del carrito
 * Actualiza: contador, items, totales
 */
function actualizarCarrito() {
    console.log('🔄 Actualizando vista del carrito...');
    
    // Actualizar contador en navbar
    actualizarContador();
    
    // Actualizar items en sidebar
    actualizarItemsCarrito();
    
    // Actualizar totales
    actualizarTotales();
}

/**
 * Actualizar el contador de items en el navbar
 */
function actualizarContador() {
    const cartCount = document.getElementById('cartCount');
    const cantidad = obtenerCantidadTotal();
    
    if (cantidad > 0) {
        cartCount.textContent = cantidad;
        cartCount.style.display = 'inline-block';
    } else {
        cartCount.style.display = 'none';
    }
}

/**
 * Actualizar la lista de items en el carrito (sidebar)
 */
function actualizarItemsCarrito() {
    const cartItemsContainer = document.getElementById('cartItems');
    
    if (carrito.length === 0) {
        // Carrito vacío
        cartItemsContainer.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                <p class="text-muted">Tu carrito está vacío</p>
            </div>
        `;
        return;
    }
    
    // Generar HTML para cada item
    let html = '<div class="cart-items-list">';
    
    carrito.forEach(producto => {
        html += `
            <div class="cart-item">
                <div class="cart-item-image">
                    <img src="${producto.imagen}" alt="${producto.nombre}">
                </div>
                
                <div class="cart-item-details">
                    <h6 class="cart-item-nombre">${producto.nombre}</h6>
                    <p class="cart-item-precio">$${producto.precio.toFixed(2)}</p>
                </div>
                
                <div class="cart-item-controls">
                    <div class="quantity-control">
                        <button class="btn-qty" onclick="actualizarCantidad(${producto.id}, ${producto.cantidad - 1})">
                            <i class="fas fa-minus"></i>
                        </button>
                        <input type="number" class="qty-input" value="${producto.cantidad}" 
                               onchange="actualizarCantidad(${producto.id}, this.value)" min="1">
                        <button class="btn-qty" onclick="actualizarCantidad(${producto.id}, ${producto.cantidad + 1})">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    
                    <p class="cart-item-subtotal">$${(producto.precio * producto.cantidad).toFixed(2)}</p>
                    
                    <button class="btn-remove" onclick="eliminarDelCarrito(${producto.id})" 
                            title="Eliminar del carrito">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    cartItemsContainer.innerHTML = html;
}

/**
 * Actualizar los totales en el carrito (subtotal, impuesto, total)
 */
function actualizarTotales() {
    const subtotal = calcularSubtotal();
    const impuesto = calcularImpuesto();
    const total = calcularTotal();
    
    const cartTotalElement = document.getElementById('cartTotal');
    
    if (cartTotalElement) {
        cartTotalElement.innerHTML = `
            <div class="totales-detalle">
                <div class="total-row">
                    <span>Subtotal:</span>
                    <span>$${subtotal.toFixed(2)}</span>
                </div>
                <div class="total-row">
                    <span>IVA (16%):</span>
                    <span>$${impuesto.toFixed(2)}</span>
                </div>
                <div class="total-row font-weight-bold">
                    <strong>Total:</strong>
                    <strong>$${total.toFixed(2)}</strong>
                </div>
            </div>
        `;
    }
}


// ========== FUNCIONES DE INTERFAZ ==========

/**
 * Abrir el sidebar del carrito
 */
function abrirCarrito() {
    console.log('🔓 Abriendo carrito...');
    
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    
    if (sidebar) {
        sidebar.classList.add('active');
    }
    if (overlay) {
        overlay.classList.add('active');
    }
}

/**
 * Cerrar el sidebar del carrito
 */
function cerrarCarrito() {
    console.log('🔒 Cerrando carrito...');
    
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    
    if (sidebar) {
        sidebar.classList.remove('active');
    }
    if (overlay) {
        overlay.classList.remove('active');
    }
}

/**
 * Configurar listeners para los botones del carrito
 */
function configurarListeners() {
    // Botón para abrir carrito en navbar
    const btnCarrito = document.getElementById('btnCarrito');
    if (btnCarrito) {
        btnCarrito.addEventListener('click', (e) => {
            e.preventDefault();
            abrirCarrito();
        });
    }
    
    // Botón para cerrar carrito
    const closeCart = document.getElementById('closeCart');
    if (closeCart) {
        closeCart.addEventListener('click', cerrarCarrito);
    }
    
    // Overlay para cerrar carrito al hacer click
    const cartOverlay = document.getElementById('cartOverlay');
    if (cartOverlay) {
        cartOverlay.addEventListener('click', cerrarCarrito);
    }
    
    // Botón continuar comprando
    const continueShopping = document.getElementById('continueShopping');
    if (continueShopping) {
        continueShopping.addEventListener('click', cerrarCarrito);
    }
    
    // Botón de checkout
    const checkoutBtn = document.getElementById('checkoutBtn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', procesarCheckout);
    }
}

/**
 * Procesar el checkout (compra)
 */
function procesarCheckout() {
    if (carrito.length === 0) {
        alert('Tu carrito está vacío');
        return;
    }
    
    const total = calcularTotal();
    const confirmacion = confirm(`¿Proceder con la compra? Total: $${total.toFixed(2)}`);
    
    if (confirmacion) {
        console.log('💳 Procesando compra...');
        console.log('📦 Carrito:', carrito);
        console.log('💰 Total:', total);
        
        // Aquí iría la integración con el servidor para procesar el pago
        // Por ahora, mostramos un mensaje de éxito
        alert(`✅ Compra procesada exitosamente!\nTotal: $${total.toFixed(2)}`);
        
        // Vaciar carrito después de compra exitosa
        carrito = [];
        guardarCarrito();
        actualizarCarrito();
        cerrarCarrito();
    }
}


// ========== FUNCIONES AUXILIARES ==========

/**
 * Obtener información del carrito en formato JSON
 * @returns {Object} Objeto con información del carrito
 */
function obtenerInfoCarrito() {
    return {
        items: carrito,
        cantidad_total: obtenerCantidadTotal(),
        subtotal: calcularSubtotal(),
        impuesto: calcularImpuesto(),
        total: calcularTotal()
    };
}

/**
 * Mostrar carrito en la consola (para debugging)
 */
function debugCarrito() {
    console.group('🐛 DEBUG CARRITO');
    console.table(carrito);
    console.log('ℹ️ Info del carrito:', obtenerInfoCarrito());
    console.groupEnd();
}

// Exponer funciones globalmente (para debugging)
window.debugCarrito = debugCarrito;
window.agregarAlCarrito = agregarAlCarrito;
window.eliminarDelCarrito = eliminarDelCarrito;
window.actualizarCantidad = actualizarCantidad;
window.vaciarCarrito = vaciarCarrito;
window.abrirCarrito = abrirCarrito;
window.cerrarCarrito = cerrarCarrito;

console.log('✅ Carrito.js cargado correctamente');
