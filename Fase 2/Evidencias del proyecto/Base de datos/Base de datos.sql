<<<<<<< HEAD
-- Tabla Usuarios
CREATE TABLE Usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    teléfono VARCHAR(15),
    dirección VARCHAR(255),
    fecha_registro DATE
);

-- Tabla Credenciales
CREATE TABLE Credenciales (
    credencial_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    fecha_ultima_conexion DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla Categorias
CREATE TABLE Categorias (
    categoria_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

-- Tabla Productos
CREATE TABLE Productos (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id INT,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10, 2),
    stock INT,
    imagen MEDIUMBLOB,  -- Imagen de producto en formato BLOB
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id)
);

-- Tabla Inventario
CREATE TABLE Inventario (
    inventario_id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    cantidad_disponible INT,
    cantidad_reservada INT,
    fecha_actualizacion DATE,
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

-- Tabla Carrito
CREATE TABLE Carrito (
    carrito_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    fecha_creacion DATE,
    estado VARCHAR(20),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla Carrito_Productos (relación muchos a muchos entre Carrito y Productos)
CREATE TABLE Carrito_Productos (
    carrito_producto_id INT AUTO_INCREMENT PRIMARY KEY,
    carrito_id INT,
    producto_id INT,
    cantidad INT,
    subtotal DECIMAL(10, 2),
    FOREIGN KEY (carrito_id) REFERENCES Carrito(carrito_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

-- Tabla Pedidos
CREATE TABLE Pedidos (
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    fecha_pedido DATE,
    total DECIMAL(10, 2),
    estado VARCHAR(20),
    fecha_entrega DATE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla Pedidos_Productos (relación muchos a muchos entre Pedidos y Productos)
CREATE TABLE Pedidos_Productos (
    pedido_producto_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    producto_id INT,
    cantidad INT,
    subtotal DECIMAL(10, 2),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

-- Tabla Pagos
CREATE TABLE Pagos (
    pago_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    monto DECIMAL(10, 2),
    fecha_pago DATE,
    metodo_pago VARCHAR(50),
    estado_pago VARCHAR(20),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id)
);

-- Tabla Entrega
CREATE TABLE Entrega (
    entrega_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    direccion_entrega VARCHAR(255),
    fecha_envio DATE,
    estado_entrega VARCHAR(20),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id)
);

-- Tabla Descuentos
CREATE TABLE Descuentos (
    descuento_id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    porcentaje_descuento DECIMAL(5, 2),
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);
=======
-- Tabla Usuarios
CREATE TABLE Usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    teléfono VARCHAR(15),
    dirección VARCHAR(255),
    fecha_registro DATE
);

-- Tabla Credenciales
CREATE TABLE Credenciales (
    credencial_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    fecha_ultima_conexion DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla Categorias
CREATE TABLE Categorias (
    categoria_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

-- Tabla Productos
CREATE TABLE Productos (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id INT,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10, 2),
    stock INT,
    imagen MEDIUMBLOB,  -- Imagen de producto en formato BLOB
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id)
);

-- Tabla Inventario
CREATE TABLE Inventario (
    inventario_id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    cantidad_disponible INT,
    cantidad_reservada INT,
    fecha_actualizacion DATE,
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

-- Tabla Carrito
CREATE TABLE Carrito (
    carrito_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    fecha_creacion DATE,
    estado VARCHAR(20),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla Carrito_Productos (relación muchos a muchos entre Carrito y Productos)
CREATE TABLE Carrito_Productos (
    carrito_producto_id INT AUTO_INCREMENT PRIMARY KEY,
    carrito_id INT,
    producto_id INT,
    cantidad INT,
    subtotal DECIMAL(10, 2),
    FOREIGN KEY (carrito_id) REFERENCES Carrito(carrito_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

-- Tabla Pedidos
CREATE TABLE Pedidos (
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    fecha_pedido DATE,
    total DECIMAL(10, 2),
    estado VARCHAR(20),
    fecha_entrega DATE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla Pedidos_Productos (relación muchos a muchos entre Pedidos y Productos)
CREATE TABLE Pedidos_Productos (
    pedido_producto_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    producto_id INT,
    cantidad INT,
    subtotal DECIMAL(10, 2),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

-- Tabla Pagos
CREATE TABLE Pagos (
    pago_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    monto DECIMAL(10, 2),
    fecha_pago DATE,
    metodo_pago VARCHAR(50),
    estado_pago VARCHAR(20),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id)
);

-- Tabla Entrega
CREATE TABLE Entrega (
    entrega_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    direccion_entrega VARCHAR(255),
    fecha_envio DATE,
    estado_entrega VARCHAR(20),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id)
);

-- Tabla Descuentos
CREATE TABLE Descuentos (
    descuento_id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    porcentaje_descuento DECIMAL(5, 2),
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a
