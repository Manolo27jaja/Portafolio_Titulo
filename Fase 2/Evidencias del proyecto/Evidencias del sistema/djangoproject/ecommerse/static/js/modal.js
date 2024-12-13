// Obtener elementos del DOM
var modal = document.getElementById("myModal");
var agregarCarritoBtn = document.getElementById("agregarCarrito");
var closeModalBtn = document.getElementsByClassName("close")[0];

// Manejar el clic en "Agregar al carrito"
agregarCarritoBtn.onclick = function(event) {
    event.preventDefault();  // Evita que el enlace redireccione

    const productoId = agregarCarritoBtn.getAttribute("data-producto-id");

    // Realizar la solicitud AJAX para agregar el producto al carrito
    fetch(`/agregar/${productoId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ producto_id: productoId })
    })
    .then(response => {
        // Verifica si la respuesta es JSON
        if (response.headers.get("content-type")?.includes("application/json")) {
            return response.json();
        } else {
            throw new Error("La respuesta no es JSON");
        }
    })
    .then(data => {
        console.log("Respuesta del servidor:", data);
        if (data.status === "Producto agregado al carrito") {
            // Muestra el modal
            modal.style.display = "block";
            
            // Actualiza la cantidad en el modal si ya existe, o la crea si es nueva
            const cantidadElemento = document.getElementById("cantidad-" + productoId);
            if (cantidadElemento) {
                // Si el elemento existe, actualiza su contenido
                cantidadElemento.textContent = data.nueva_cantidad;
                const filaProducto = document.querySelector(`#fila-${productoId}`);
                if (filaProducto) {
                    filaProducto.querySelector(".nombre-producto").textContent = data.nombre_producto;
                    filaProducto.querySelector(`#acumulado-${productoId}`).textContent = `Total: $ ${data.precio_producto}`;
                }
            } else {
                // Si el elemento no existe, añade una nueva fila en el carrito
                const carritoTabla = document.querySelector(".table tbody");
                const nuevaFila = document.createElement("tr");
                nuevaFila.id = `fila-${productoId}`;
                nuevaFila.innerHTML = `
                    <td class="nombre-producto">${data.nombre_producto || "Producto no definido"}</td>
                    <td>
                        <span id="acumulado-${productoId}">Total: $ ${data.precio_producto || "0"}</span>
                    </td>
                    <td>
                        <a href="#" class="badge btn btn-dark badge-dark" onclick="actualizarCantidad('${productoId}', 'add')">+</a>
                        <span id="cantidad-${productoId}">${data.nueva_cantidad}</span>
                        <a href="#" class="badge btn btn-dark badge-dark" onclick="actualizarCantidad('${productoId}', 'sub')">-</a>
                    </td>
                `;
                carritoTabla.appendChild(nuevaFila);
            }
            
            // Actualiza el total del carrito en el modal si es necesario
            const totalCarritoElemento = document.getElementById("total-carrito");
            if (totalCarritoElemento) {
                totalCarritoElemento.textContent = "$ " + data.total_carrito;
            }
        }
    })
    .catch(error => console.error("Error:", error));
};
// Función para obtener el CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// _______________________________________________________
// _________________________________________Cerrar el modal cuando se hace clic en la "X"
closeModalBtn.onclick = function() {
    modal.style.display = "none";
};
// Cerrar el modal cuando se hace clic fuera del modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};
//_____________________________________________________________________________________



//__________________________________________________________________




//___________________________________________________________________

function actualizarCarritoModal(data) {
    // Reemplaza las filas existentes del carrito con los nuevos datos
    const carritoTabla = document.querySelector(".table tbody");
    carritoTabla.innerHTML = ''; // Limpiar el contenido actual

    data.carrito.items.forEach(item => {
        const nuevaFila = document.createElement('tr');
        nuevaFila.innerHTML = `
            <td>${item.nombre}</td>
            <td><span id="acumulado-${item.producto_id}">Total: ${item.acumulado}</span></td>
            <td>
                <a href="#" class="badge btn btn-dark badge-dark" onclick="actualizarCantidad('${item.producto_id}', 'add')">+</a>
                <span id="cantidad-${item.producto_id}">${item.cantidad}</span>
                <a href="#" class="badge btn btn-dark badge-dark" onclick="actualizarCantidad('${item.producto_id}', 'sub')">-</a>
            </td>
        `;
        carritoTabla.appendChild(nuevaFila);
    });

    // Actualiza el total del carrito
    const totalCarritoElemento = document.getElementById("total-carrito");
    if (totalCarritoElemento) {
        totalCarritoElemento.textContent = '$ ' + data.carrito.total;
    }
}

function actualizarCantidad(productoId, accion) {
    const url = accion === 'add' ? `/aumentar/${productoId}/` : `/restar/${productoId}/`;
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ producto_id: productoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'Cantidad actualizada') {
            // Actualiza la cantidad y el acumulado en el modal
            const cantidadElemento = document.getElementById(`cantidad-${productoId}`);
            if (cantidadElemento) {
                cantidadElemento.textContent = data.nueva_cantidad;
            }

            const acumuladoElemento = document.getElementById(`acumulado-${productoId}`);
            if (acumuladoElemento) {
                acumuladoElemento.textContent = `Total: ${data.acumulado}`;
            }

            // Actualiza el total del carrito
            const totalCarritoElemento = document.getElementById("total-carrito");
            if (totalCarritoElemento) {
                totalCarritoElemento.textContent = '$ ' + data.total_carrito;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}
