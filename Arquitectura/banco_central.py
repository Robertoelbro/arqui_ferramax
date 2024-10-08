import bcchapi
from bcchapi import Siete
import json
import numpy as np
import requests

# Pedir credenciales al usuario
print("Ingresa los datos de tu credencial")
correo = input("Correo: ")
contraseña = input("Contraseña: ")

# Inicializar la clase Siete con las credenciales
siete = Siete(correo, contraseña)

opc = 0  # Inicializamos la variable opc

# Bucle while que continuará hasta que se seleccione la opción 4 (Salir)
while opc != 4:
  print("\nTe presento la API del Banco Central")
  print("1. Buscar sin número de serie")
  print("2. Buscar por número de serie")
  print("3. Mostrar métodos de 'Siete'")
  print("4. Salir")

  opc = int(input("Selecciona una opción: "))

  if opc == 1:
    busqueda = input("Ingresa tu palabra de búsqueda: ")
    resultado_buscar = siete.buscar(busqueda)
    print("Resultado de la búsqueda:")
    print(resultado_buscar)

  elif opc == 2:
    serie = input("Ingresa tu N° de serie: ")
    fecha_desde = input("Ingresa desde qué fecha (YYYY-MM-DD): ")
    fecha_hasta = input("Ingresa hasta qué fecha (YYYY-MM-DD): ")
    datos = siete.cuadro(
    series=serie,
    desde=fecha_desde,
    hasta=fecha_hasta
    )
    print("Datos obtenidos:")
    print(datos)
    
  elif opc == 3:
    metodos_disponibles = dir(siete)
    metodos_publicos = [metodo for metodo in metodos_disponibles if not metodo.startswith('_')]
    print("Métodos disponibles en la clase Siete:")
    for metodo in metodos_publicos:
      print(metodo)

  elif opc == 4:
    print("Gracias por su preferencia. Saliendo del programa...")

  else:
    print("Opción no válida. Intenta de nuevo.")
