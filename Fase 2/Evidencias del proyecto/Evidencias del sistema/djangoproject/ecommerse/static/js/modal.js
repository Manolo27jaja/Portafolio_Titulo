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
            } else {
                // Si el elemento no existe, añade una nueva fila en el carrito
                const carritoTabla = document.querySelector(".table tbody");
                const nuevaFila = document.createElement("tr");
                nuevaFila.innerHTML = `
                    <td>${data.nombre_producto}</td>
                    <td>${data.precio_producto}</td>
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
// Cerrar el modal cuando se hace clic en la "X"
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


function actualizarCantidad(productoId, accion) {
    fetch(`/restar/${productoId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ producto_id: productoId, accion: accion })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "Cantidad actualizada") {
            // Actualiza solo la cantidad del producto en el DOM
            document.getElementById("cantidad-" + productoId).textContent = data.nueva_cantidad;
            
            // Actualiza el total del carrito en el modal
            document.getElementById("total-carrito").textContent = "$ " + data.total_carrito;
        }
    })
    .catch(error => console.error("Error:", error));
}


//__________________________________________________________________

function actualizarCantidad(productoId, accion) {
    const url = accion === "add" ? `/aumentar/${productoId}/` : `/restar/${productoId}/`;

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ producto_id: productoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "Cantidad actualizada") {
            // Actualiza solo la cantidad del producto en el DOM
            document.getElementById("cantidad-" + productoId).textContent = data.nueva_cantidad;
            
            // Actualiza el total del carrito en el modal
            document.getElementById("total-carrito").textContent = "$ " + data.total_carrito;
        }
    })
    .catch(error => console.error("Error:", error));
}


//___________________________________________________________________
