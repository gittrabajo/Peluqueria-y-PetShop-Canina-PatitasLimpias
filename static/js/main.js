// Funcionalidad JavaScript para Patitas Limpias

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll para los links de navegación
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Animación de scroll reveal
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observar todas las tarjetas
    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease-out';
        observer.observe(card);
    });

    // Formulario de agenda
    const agendaForm = document.querySelector('#agenda form');
    if (agendaForm) {
        agendaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const nombreMascota = this.querySelector('input[placeholder*="Firulais"]').value;
            const fecha = this.querySelector('input[type="date"]').value;
            const hora = this.querySelector('input[type="time"]').value;
            
            if (nombreMascota && fecha && hora) {
                alert(`¡Cita reservada para ${nombreMascota}!\n\nFecha: ${fecha}\nHora: ${hora}\n\nNos veremos pronto.`);
                this.reset();
            } else {
                alert('Por favor completa todos los campos');
            }
        });
    }

    // Formulario de contacto
    const contactForm = document.querySelector('#contacto form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const nombre = this.querySelector('input[placeholder*="nombre"]').value;
            const email = this.querySelector('input[type="email"]').value;
            const mensaje = this.querySelector('textarea').value;
            
            if (nombre && email && mensaje) {
                alert(`¡Gracias ${nombre}!\n\nHemos recibido tu mensaje.\nNos pondremos en contacto pronto a través de ${email}`);
                this.reset();
            } else {
                alert('Por favor completa todos los campos');
            }
        });
    }

    // Buttons para agregar al carrito
    const cartButtons = document.querySelectorAll('.fa-shopping-cart').forEach(btn => {
        btn.parentElement.addEventListener('click', function(e) {
            e.preventDefault();
            
            const productName = this.closest('.card').querySelector('h5').textContent;
            const price = this.closest('.card').querySelector('h5:nth-of-type(2)').textContent;
            
            alert(`${productName} agregado al carrito`);
        });
    });

    // Scroll animar navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });

    // Contador de visitas (ejemplo local)
    let visitCount = localStorage.getItem('visitCount') || 0;
    visitCount = parseInt(visitCount) + 1;
    localStorage.setItem('visitCount', visitCount);
    console.log(`Visitas: ${visitCount}`);

    // Validación de email simple
    function validarEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Tooltips (Bootstrap)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Función para redirigir a WhatsApp
function abrirWhatsApp() {
    const numero = '34123456789';
    const mensaje = 'Hola! Me gustaría conocer más sobre sus servicios de peluquería y petshop.';
    const url = `https://wa.me/${numero}?text=${encodeURIComponent(mensaje)}`;
    window.open(url, '_blank');
}

// Función para cambiar idioma (ejemplo)
function cambiarIdioma(idioma) {
    console.log(`Idioma cambiado a: ${idioma}`);
    // Aquí irías las traducciones
}
