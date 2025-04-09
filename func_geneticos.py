import constantes as const
import numpy as np
import h5py

def fitness(individuo):
    """
    Calcula la función de fitness de un individuo.
    La función de fitness es la suma de los valores de los genes del individuo.
    """
    # Separar columnas para mayor claridad (opcional)
    # Variables
    dist_manzana = individuo[:, 3]
    dist_pared = individuo[:, 4]
    score = individuo[:, 5]

    n = len(individuo)                     # duración del individuo
    score_total = np.sum(score)            # total manzanas comidas
    max_duracion = 100                     # valor que defines tú

    # Cálculo del fitness
    fitness = (
        np.sum(const.ALPHA * score - const.BETA * dist_manzana + const.GAMMA * dist_pared)
        - const.DELTA * (n / (score_total + 1))
        - const.EPSILON * (1 - (n / max_duracion))
    )

    return fitness

def guardar_matriz(individuo, nombre_archivo="matriz_decision.txt"):
    with h5py.File(nombre_archivo, "w") as f:
        # Guardar la matriz como un dataset
        f.create_dataset(nombre_archivo, data=individuo)

def leer_matriz(nombre_archivo="matriz_decision.txt"):
    with h5py.File(nombre_archivo, "r") as f:
        # Leer el dataset y convertirlo a un array de numpy
        matriz = np.array(f[nombre_archivo])
    return matriz


def distancia_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])