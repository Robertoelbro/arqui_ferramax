import sqlite3
import os

# Ruta del archivo de base de datos
db_file = 'productos.db'

# Verificar la ruta del archivo
print("Ruta del archivo de base de datos:", os.path.abspath(db_file))

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Crear la tabla de productos si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL
)
''')
conn.commit()  # Guardar la creación de la tabla

# Función para crear un nuevo producto
def crear_producto(nombre, precio, cantidad):
    cursor.execute('''
    INSERT INTO productos (nombre, precio, cantidad)
    VALUES (?, ?, ?)
    ''', (nombre, precio, cantidad))
    conn.commit()  # Guardar cambios en la base de datos
    print(f"Producto '{nombre}' creado con éxito.")

# Función para listar todos los productos
def listar_productos():
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()

    if productos:
        print("\nLista de productos en la base de datos:")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}, Cantidad: {producto[3]}")
    else:
        print("No hay productos en la base de datos.")

# Función para buscar un producto por su nombre
def buscar_producto(nombre_producto):
    cursor.execute('SELECT precio, cantidad FROM productos WHERE nombre = ?', (nombre_producto,))
    producto = cursor.fetchone()

    if producto:
        print(f"Precio: {producto[0]}, Cantidad: {producto[1]}")
    else:
        print(f"El producto '{nombre_producto}' no existe en la base de datos.")

# Menú principal
while True:
    opcion = input("\n¿Qué deseas hacer? (crear/buscar/listar/salir): ").lower()

    if opcion == "crear":
        # Pedir los detalles del producto al usuario
        nombre = input("Introduce el nombre del producto: ")
        precio = float(input("Introduce el precio del producto: "))
        cantidad = int(input("Introduce la cantidad del producto: "))
        
        # Llamar a la función para crear el producto
        crear_producto(nombre, precio, cantidad)

    elif opcion == "buscar":
        # Pedir el nombre del producto para buscar
        nombre_producto = input("Introduce el nombre del producto que quieres consultar: ")
        buscar_producto(nombre_producto)

    elif opcion == "listar":
        # Llamar a la función para listar todos los productos
        listar_productos()

    elif opcion == "salir":
        break

    else:
        print("Opción no válida. Intenta de nuevo.")

# Cerrar la conexión a la base de datos al salir
conn.close()


    
