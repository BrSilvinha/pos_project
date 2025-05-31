// Archivo main.js para el Sistema POS

// Función para mostrar tooltips de Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-cerrar alertas después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Función para confirmar eliminación
function confirmarEliminacion(event, mensaje) {
    if (!confirm(mensaje || '¿Está seguro de que desea eliminar este elemento?')) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Función para actualizar el contador de caracteres en textareas
function actualizarContador(textareaId, contadorId, maxLength) {
    const textarea = document.getElementById(textareaId);
    const contador = document.getElementById(contadorId);
    
    if (textarea && contador) {
        textarea.addEventListener('input', function() {
            const caracteresRestantes = maxLength - this.value.length;
            contador.textContent = caracteresRestantes;
            
            // Cambiar color si se acerca al límite
            if (caracteresRestantes < 50) {
                contador.style.color = '#dc3545'; // Rojo
            } else if (caracteresRestantes < 100) {
                contador.style.color = '#ffc107'; // Amarillo
            } else {
                contador.style.color = '#6c757d'; // Gris
            }
        });
    }
}

// Función para búsqueda en tiempo real
function busquedaEnTiempoReal(inputId, contenedorId) {
    const input = document.getElementById(inputId);
    const contenedor = document.getElementById(contenedorId);
    
    if (input && contenedor) {
        input.addEventListener('keyup', function() {
            const busqueda = this.value.toLowerCase();
            const elementos = contenedor.querySelectorAll('.elemento-busqueda');
            
            elementos.forEach(function(elemento) {
                const texto = elemento.textContent.toLowerCase();
                if (texto.includes(busqueda)) {
                    elemento.style.display = '';
                } else {
                    elemento.style.display = 'none';
                }
            });
        });
    }
}

// Función para formatear números como moneda
function formatearMoneda(numero) {
    return new Intl.NumberFormat('es-PE', {
        style: 'currency',
        currency: 'PEN'
    }).format(numero);
}

// Función para mostrar notificaciones toast
function mostrarToast(mensaje, tipo = 'info') {
    const toastContainer = document.getElementById('toast-container') || crearContenedorToast();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${tipo} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${mensaje}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Eliminar el toast después de que se oculte
    toast.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Crear contenedor para toasts si no existe
function crearContenedorToast() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}