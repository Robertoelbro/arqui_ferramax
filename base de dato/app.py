import sqlite3

conn = sqlite3.connect('productos.db')

# Crear un cursor
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL
)
''')

productos = [
    ('clavos', 1500, 100),
    ('tornillos', 4500, 200),
    ('desatornillador', 4000, 150),
    ('martillo', 5000, 50),
]
cursor.executemany('''
INSERT INTO productos (nombre, precio, cantidad)
VALUES (?, ?, ?)
''', productos)
conn.commit()


def buscar_producto(nombre_producto):
    cursor.execute('SELECT precio, cantidad FROM productos WHERE nombre = ?', (nombre_producto,))
    producto = cursor.fetchone()

    if producto:
        print(f"Precio: {producto[0]}, Cantidad: {producto[1]}")
    else:
        print(f"El producto '{nombre_producto}' no existe en la base de datos.")


nombre_producto = input("Introduce el nombre del producto que quieres consultar: ")

buscar_producto(nombre_producto)

conn.close()
    
