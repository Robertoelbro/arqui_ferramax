import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk  # Necesario para mostrar las imágenes

# Conexión a la base de datos
conn = sqlite3.connect('productos.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS productos')

# Crear tabla productos si no existe, agregando descripcion y foto
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL,
    descripcion TEXT,
    foto TEXT  -- Ruta de la imagen
)
''')

# Crear tabla catalogo si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS catalogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
''')

conn.commit()

def buscar_producto():
    nombre_producto = entry_nombre.get().strip()  # Obtener el nombre del producto desde el campo de entrada
    cursor.execute('SELECT precio, cantidad, descripcion, foto FROM productos WHERE nombre = ?', (nombre_producto,))
    producto = cursor.fetchone()

    if producto:
        precio, cantidad, descripcion, foto = producto

        # Formatear el precio en pesos chilenos
        precio_formateado = f"${precio:,.0f} CLP"  # Agrega el símbolo y formatea los miles
        
        # Mostrar resultados
        resultado.set(f"Precio: {precio_formateado}, Cantidad: {cantidad}, Descripción: {descripcion}")

        # Mostrar la imagen del producto si existe
        if foto and foto.strip():  # Verificar que la ruta de la foto no esté vacía
            try:
                img = Image.open(foto)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar imagen
                img_tk = ImageTk.PhotoImage(img)
                label_foto.config(image=img_tk)
                label_foto.image = img_tk  # Mantener referencia para que no se recolecte como basura
            except Exception as e:
                label_foto.config(image='')  # Limpiar la imagen en caso de error
                label_foto['text'] = "Imagen no disponible"
        else:
            label_foto.config(image='')  # Limpiar la imagen si no hay foto
            label_foto['text'] = "Sin foto"
    else:
        resultado.set(f"El producto '{nombre_producto}' no existe en la base de datos.")



# Función para agregar un nuevo producto
def agregar_producto():
    def guardar_producto():
        try:
            nombre = entry_nombre_nuevo.get().strip()
            precio = float(entry_precio_nuevo.get())
            cantidad = int(entry_cantidad_nuevo.get())
            descripcion = entry_descripcion_nueva.get("1.0", tk.END).strip()
            foto = entry_foto_nueva.get()

            if not nombre or not descripcion or not foto:
                messagebox.showwarning("Campos vacíos", "Por favor, rellena todos los campos y selecciona una foto.")
                return
            
            # Validar que el precio y cantidad sean correctos
            if precio <= 0 or cantidad < 0:
                messagebox.showwarning("Datos incorrectos", "El precio debe ser mayor a 0 y la cantidad no puede ser negativa.")
                return

            # Insertar producto en la base de datos
            cursor.execute('''
            INSERT INTO productos (nombre, precio, cantidad, descripcion, foto)
            VALUES (?, ?, ?, ?, ?)
            ''', (nombre, precio, cantidad, descripcion, foto))
            conn.commit()
            
            # Agregar producto al catálogo
            producto_id = cursor.lastrowid
            cursor.execute('INSERT INTO catalogo (producto_id) VALUES (?)', (producto_id,))
            conn.commit()

            messagebox.showinfo("Producto agregado", f"Producto '{nombre}' agregado con éxito.")
            ventana_agregar.destroy()

        except ValueError:
            messagebox.showwarning("Error de tipo", "Por favor, asegúrate de que el precio y la cantidad sean valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al guardar el producto: {e}")

    def seleccionar_foto():
        ruta_foto = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.png")])
        if ruta_foto:
            entry_foto_nueva.delete(0, tk.END)
            entry_foto_nueva.insert(0, ruta_foto)

    # Ventana para agregar producto
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Producto")

    tk.Label(ventana_agregar, text="Nombre del producto:").pack(pady=5)
    entry_nombre_nuevo = tk.Entry(ventana_agregar)
    entry_nombre_nuevo.pack(pady=5)

    tk.Label(ventana_agregar, text="Precio del producto:").pack(pady=5)
    entry_precio_nuevo = tk.Entry(ventana_agregar)
    entry_precio_nuevo.pack(pady=5)

    tk.Label(ventana_agregar, text="Cantidad del producto:").pack(pady=5)
    entry_cantidad_nuevo = tk.Entry(ventana_agregar)
    entry_cantidad_nuevo.pack(pady=5)

    tk.Label(ventana_agregar, text="Descripción del producto:").pack(pady=5)
    entry_descripcion_nueva = tk.Text(ventana_agregar, height=5)
    entry_descripcion_nueva.pack(pady=5)

    tk.Label(ventana_agregar, text="Ruta de la foto:").pack(pady=5)
    entry_foto_nueva = tk.Entry(ventana_agregar)
    entry_foto_nueva.pack(pady=5)
    
    boton_seleccionar_foto = tk.Button(ventana_agregar, text="Seleccionar foto", command=seleccionar_foto)
    boton_seleccionar_foto.pack(pady=5)

    tk.Button(ventana_agregar, text="Guardar", command=guardar_producto).pack(pady=10)

# Función para mostrar el catálogo de productos
def mostrar_catalogo():
    ventana_catalogo = tk.Toplevel(root)
    ventana_catalogo.title("Catálogo de Productos")

    # Consulta SQL ajustada para evitar duplicados y obtener la cantidad
    cursor.execute(''' 
    SELECT DISTINCT p.nombre, p.precio, p.cantidad, p.descripcion, p.foto 
    FROM productos p 
    JOIN catalogo c ON p.id = c.producto_id
    ''')

    productos = cursor.fetchall()

    if not productos:
        tk.Label(ventana_catalogo, text="No hay productos en el catálogo").pack(pady=10)
        return

    # Mostrar cada producto una vez
    for producto in productos:
        nombre, precio, cantidad, descripcion, foto = producto

        precio_formateado = f"${precio:,.0f} CLP"  # Agrega el símbolo y formatea los miles
        
        # Mostrar los detalles del producto
        tk.Label(ventana_catalogo, text=f"Nombre: {nombre}").pack(pady=5)
        tk.Label(ventana_catalogo, text=f"Precio: {precio_formateado}").pack(pady=5)
        tk.Label(ventana_catalogo, text=f"Cantidad: {cantidad}").pack(pady=5)  # Mostrar cantidad
        tk.Label(ventana_catalogo, text=f"Descripción: {descripcion}").pack(pady=5)

        # Mostrar imagen si existe
        if foto and foto.strip():  # Verificar que la ruta de la foto no esté vacía
            try:
                img = Image.open(foto)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar imagen
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(ventana_catalogo, image=img_tk)
                img_label.pack(pady=5)
                img_label.image = img_tk  # Guardar referencia para evitar garbage collection
            except Exception as e:
                tk.Label(ventana_catalogo, text="Imagen no disponible").pack(pady=5)
        else:
            tk.Label(ventana_catalogo, text="Sin imagen").pack(pady=5)

# Función para eliminar un producto
def eliminar_producto():
    def confirmar_eliminacion():
        nombre_producto = entry_nombre_eliminar.get().strip()

        # Verificar si el producto existe
        cursor.execute('SELECT id FROM productos WHERE nombre = ?', (nombre_producto,))
        producto = cursor.fetchone()

        if producto:
            producto_id = producto[0]

            # Eliminar el producto de la tabla 'productos'
            cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
            conn.commit()

            # Eliminar el producto de la tabla 'catalogo'
            cursor.execute('DELETE FROM catalogo WHERE producto_id = ?', (producto_id,))
            conn.commit()

            messagebox.showinfo("Producto eliminado", f"El producto '{nombre_producto}' ha sido eliminado con éxito.")
            ventana_eliminar.destroy()
        else:
            messagebox.showerror("Error", f"El producto '{nombre_producto}' no existe en la base de datos.")

    # Ventana para eliminar producto
    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.title("Eliminar Producto")

    tk.Label(ventana_eliminar, text="Introduce el nombre del producto que deseas eliminar:").pack(pady=5)
    entry_nombre_eliminar = tk.Entry(ventana_eliminar)
    entry_nombre_eliminar.pack(pady=5)

    tk.Button(ventana_eliminar, text="Eliminar", command=confirmar_eliminacion).pack(pady=10)

# Función para salir de la aplicación
def salir():
    root.quit()

# Función para mostrar información "Acerca de"
def mostrar_acerca_de():
    messagebox.showinfo("Acerca de", "Aplicación de gestión de productos v2.0\nCreada con Tkinter y SQLite")

# Crear ventana principal
root = tk.Tk()
root.title("Consulta de Productos")

# Menú
menu_bar = tk.Menu(root)

# Menú Archivo
menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_archivo.add_command(label="Salir", command=salir)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

# Menú Productos
menu_productos = tk.Menu(menu_bar, tearoff=0)
menu_productos.add_command(label="Agregar Producto", command=agregar_producto)
menu_productos.add_command(label="Mostrar Catálogo", command=mostrar_catalogo)
menu_bar.add_cascade(label="Productos", menu=menu_productos)
menu_productos.add_command(label="Eliminar Producto", command=eliminar_producto)

# Menú Ayuda
menu_ayuda = tk.Menu(menu_bar, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=mostrar_acerca_de)
menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)

# Configurar la barra de menú
root.config(menu=menu_bar)

# Etiqueta y campo de entrada para el nombre del producto
label_nombre = tk.Label(root, text="Introduce el nombre del producto:")
label_nombre.pack(pady=10)

entry_nombre = tk.Entry(root)
entry_nombre.pack(pady=5)

# Botón para buscar producto
boton_buscar = tk.Button(root, text="Buscar", command=buscar_producto)
boton_buscar.pack(pady=10)

# Variable para mostrar el resultado
resultado = tk.StringVar()
label_resultado = tk.Label(root, textvariable=resultado)
label_resultado.pack(pady=10)

# Etiqueta para mostrar la foto del producto
label_foto = tk.Label(root, text="Sin foto")
label_foto.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()

# Cerrar la conexión
conn.close()
