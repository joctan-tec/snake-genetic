import numpy as np
import pandas as pd
from custom_utils import mostrar_tabla
from func_geneticos import leer_matriz
from tabulate import tabulate

print(leer_matriz().shape)

df = pd.DataFrame(leer_matriz(), columns=["columna", "fila", "direccion antes", "columna manzana", "fila manzana", "distancia pared", "score", "direccion despues"])

# Si el valor de la columna "direccion antes" es 1 cambiarlo a "Derecha", Si es 2, cambiarlo a "Izquierda", Si es 3, cambiarlo a "Arriba", Si es 4, cambiarlo a "Abajo"
df["direccion antes"] = df["direccion antes"].map({1: "Derecha", 2: "Izquierda", 3: "Arriba", 4: "Abajo"})
# Si el valor de la columna "direccion despues" es 1 cambiarlo a "Derecha", Si es 2, cambiarlo a "Izquierda", Si es 3, cambiarlo a "Arriba", Si es 4, cambiarlo a "Abajo"
df["direccion despues"] = df["direccion despues"].map({1: "Derecha", 2: "Izquierda", 3: "Arriba", 4: "Abajo"})


print(df.describe())





print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

