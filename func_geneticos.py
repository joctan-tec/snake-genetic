import constantes as const
import numpy as np

def fitness(individuo):
    """
    Calcula la función de fitness de un individuo.
    La función de fitness es la suma de los valores de los genes del individuo.
    """
    # Separar columnas para mayor claridad (opcional)
    # Variables
    dist_manzana = individuo[:, 0]
    dist_pared = individuo[:, 1]
    score = individuo[:, 2]

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


def distancia_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])