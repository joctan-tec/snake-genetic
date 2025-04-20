import constantes as const
import numpy as np
import h5py
import random

def fitness(individuo):
    """
    Calcula la función de fitness de un individuo.
    La función de fitness es la suma de los valores de los genes del individuo.
    """
    # Separar columnas para mayor claridad (opcional)
    # Variables
    # if np.array_equal(individuo, []):
    #     return 0
    
    dist_manzana = individuo[:, 4]
    dist_pared = individuo[:, 5]
    score = individuo[:, 6]

    n = len(individuo)                     # duración del individuo
    score_total = np.sum(score)            # total manzanas comidas
    max_duracion = 100                     # valor que defines tú

    # Cálculo del fitness
    fitness = (
        np.sum(const.ALPHA * score - const.BETA * dist_manzana + const.GAMMA * dist_pared)
    )

    return fitness

def guardar_matriz(individuo, nombre_archivo="matriz_decision_x.txt"):
    with h5py.File(nombre_archivo, "w") as f:
        # Guardar la matriz como un dataset
        f.create_dataset(nombre_archivo, data=individuo)

def leer_matriz(nombre_archivo="matriz_decision_x.txt"):
    try:
        with h5py.File(nombre_archivo, "r") as f:
            # Leer el dataset y convertirlo a un array de numpy
            matriz = np.array(f[nombre_archivo])
    except:
        return []
    return matriz



def seleccion_por_ranking(poblacion_ordenada, probs, k=2):
    seleccionados = random.choices(
        poblacion_ordenada,
        weights=probs,
        k=k
    )
    return seleccionados


def cruce_concatenado(padres):
    secuencias = [padre[1][0] for padre in padres]
    total_padres = len(secuencias)

    # Tomar una fracción de cada uno (por ejemplo, 1/n de cada uno)
    hijo = []
    for seq in secuencias:
        # n_bloque = max(1, len(seq) // total_padres)
        hijo.extend(seq)

    return np.array(hijo)

def cruce(padres):
    hijos = []

    # Asegurar que haya una cantidad par
    if len(padres) % 2 != 0:
        padres = padres[:-1]

    # Intercambiar la mitad de las secuencias entre los padres
    for i in range(0, len(padres), 2):
        padre1 = padres[i][1][0]
        padre2 = padres[i + 1][1][0]

        # Intercambiar la mitad de las secuencias
        mitad = len(padre1) // 2
        mitad2 = len(padre2) // 2

        parte1 = padre1[:mitad]
        parte2 = padre2[mitad2:]
        hijo1_crom = np.concatenate((parte1, parte2), axis=0)

        parte1 = padre2[:mitad]
        parte2 = padre1[mitad2:]
        hijo2_crom = np.concatenate((parte1, parte2), axis=0)

        hijos += hijo1_crom.tolist()
        hijos += hijo2_crom.tolist()

    return hijos


def fusionar_matrices(matriz_prev, nueva_tabla):
    matriz_prev = np.array(matriz_prev)
    if matriz_prev.size == 0:
        return nueva_tabla

    # Unir verticalmente y eliminar duplicados
    fusion = np.vstack((matriz_prev, nueva_tabla))

    # Eliminar movimientos duplicados (considerando filas iguales)
    fusion_sin_repetidos = np.unique(fusion, axis=0)

    return fusion_sin_repetidos

def mutar_movimientos(matriz, tasa_mutacion=0.1):
    """
    Aplica mutación solamente en la columna 6 (movimiento) de algunas filas.
    Los movimientos posibles son 0, 1, 2 o 3.
    """
    matriz_mutada = matriz.copy()
    n_filas = len(matriz)

    n_mutaciones = max(1, int(n_filas * tasa_mutacion))
    filas_a_mutar = random.sample(range(n_filas), n_mutaciones)

    for fila in filas_a_mutar:
        valor_actual = int(matriz_mutada[fila][-1])
        opciones = [1, 2, 3, 4]
        opciones.remove(valor_actual)  # evita repetir el mismo valor
        matriz_mutada[fila][-1] = np.int64(random.choice(opciones))

    return matriz_mutada




def distancia_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])