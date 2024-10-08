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