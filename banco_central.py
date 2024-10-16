import bcchapi
from bcchapi import Siete
import json
import numpy as np
import requests


siete = Siete("correo", "Contraseña")

datos=siete.buscar("antofagasta")

datos=siete.cuadro(
  series=["F032.IMC.IND.Z.Z.EP18.Z.Z.0.M", "G073.IPC.IND.2018.M"],
  nombres = ["imacec", "ipc"],
  desde="2010-01-01",
  hasta="2020-12-01",
  variacion=12,
  frecuencia="A",
  observado={"imacec":np.mean, "ipc":"last"}
)

print(datos)

tipo_cambio = siete.cuadro(
  series=["F072.TCO.PRE.Z.Z.M"],
  nombres=["tipo_cambio"],
  desde="2023-10-04",  
  hasta="2023-10-07",  
  frecuencia="D",  
  observado={"tipo_cambio": "last"}  
)

print("Tipo de cambio de los últimos 3 días:")
print(tipo_cambio)
  