const App = function() {
    this.currentIndex = 0; // Inicializa el índice del carrusel
    this.itemsPerPage = 3; // Número de productos visibles (ajusta según el CSS)
    this.track = document.getElementById('track');

    // Agrega eventos a los botones
    document.getElementById('button-prev').addEventListener('click', (event) => this.processingButton(event));
    document.getElementById('button-next').addEventListener('click', (event) => this.processingButton(event));
};

App.prototype.processingButton = function(event) {
    const btn = event.currentTarget;

    // Obtiene la cantidad total de productos
    const totalItems = this.track.children.length;

    // Calcula el máximo índice que se puede alcanzar
    const maxIndex = Math.ceil(totalItems / this.itemsPerPage) - 1;

    // Maneja el botón de anterior
    if (btn.dataset.button === "button-prev") {
        if (this.currentIndex > 0) {
            this.currentIndex--;
        }
    } else {
        // Maneja el botón de siguiente
        if (this.currentIndex < maxIndex) {
            this.currentIndex++;
        }
    }

    // Desplaza la pista
    const offset = -this.currentIndex * (100 / this.itemsPerPage);
    this.track.style.transform = `translateX(${offset}%)`;
};

const app = new App();
