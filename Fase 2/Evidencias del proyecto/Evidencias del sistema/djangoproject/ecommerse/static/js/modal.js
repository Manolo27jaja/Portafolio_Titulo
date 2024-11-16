// Obtener elementos del DOM
var modal = document.getElementById("myModal");
var openModalBtn = document.getElementById("openModal");
var closeModalBtn = document.getElementsByClassName("close")[0];

// Abrir el modal cuando se hace clic en el botón
openModalBtn.onclick = function() {
  modal.style.display = "block";
}

// Cerrar el modal cuando se hace clic en la "X"
closeModalBtn.onclick = function() {
  modal.style.display = "none";
}

// Cerrar el modal cuando se hace clic fuera del modal
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
