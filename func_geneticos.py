import constantes as const
import numpy as np
import h5py
import random



import numpy as np

def fitness(individuo):
    try:
        individuo = np.array(individuo)

        cabeza_x = individuo[:, 0]
        cabeza_y = individuo[:, 1]
        dir_antes = individuo[:, 2]
        manzana_x = individuo[:, 3]
        manzana_y = individuo[:, 4]
        dist_pared = individuo[:, 5]
        score = individuo[:, 6]
        dir_despues = individuo[:, 7]

        n = len(individuo)
        score_total = np.sum(score)
        max_duracion = 100

        # Calcular distancia a manzana
        dist_manzana = np.abs(cabeza_x - manzana_x) + np.abs(cabeza_y - manzana_y)

        # Penalización si la dirección después no se acerca a la manzana
        penalizacion_ignoradas = 0
        for i in range(n):
            dx = manzana_x[i] - cabeza_x[i]
            dy = manzana_y[i] - cabeza_y[i]
            direccion = dir_despues[i]

            # Determinar dirección óptima
            if abs(dx) > abs(dy):  # priorizamos el movimiento horizontal
                if dx < 0 and direccion != 0:  # izquierda
                    penalizacion_ignoradas += 1
                elif dx > 0 and direccion != 1:  # derecha
                    penalizacion_ignoradas += 1
            else:
                if dy < 0 and direccion != 2:  # arriba
                    penalizacion_ignoradas += 1
                elif dy > 0 and direccion != 3:  # abajo
                    penalizacion_ignoradas += 1

        penalizacion_ignoradas *= const.THETA

        # Cálculo final del fitness
        fitness = (
            np.sum(const.ALPHA * score - const.BETA * dist_manzana + const.GAMMA * dist_pared)
            - penalizacion_ignoradas
            - const.DELTA * (n / (score_total + 1))
            - const.EPSILON * (1 - (n / max_duracion))
        )

        return fitness

    except Exception as e:
        print("Error en el cálculo de fitness:", e)
        print("Tipo:", type(individuo), "Shape:", np.array(individuo).shape)
        print("Contenido:\n", individuo)
        return 0


def guardar_matriz(individuo, nombre_archivo="matriz_decision.txt"):
    with h5py.File(nombre_archivo, "w") as f:
        # Guardar la matriz como un dataset
        f.create_dataset(nombre_archivo, data=individuo)

def leer_matriz(nombre_archivo="matriz_decision.txt"):
    with h5py.File(nombre_archivo, "r") as f:
        # Leer el dataset y convertirlo a un array de numpy
        matriz = np.array(f[nombre_archivo])
    return matriz



def seleccion_por_ranking(poblacion_ordenada, probs, k=2):
    seleccionados = random.choices(
        poblacion_ordenada,
        weights=probs,
        k=k
    )
    return seleccionados

def seleccion_torneo(poblacion, k=3, cantidad_seleccionados=None):
    """
    poblacion: lista de tuplas (id, movimientos_array, tiempo, fitness)
    k: número de individuos que compiten en cada torneo
    cantidad_seleccionados: cantidad de individuos a seleccionar
    """
    if cantidad_seleccionados is None:
        cantidad_seleccionados = len(poblacion)

    seleccionados = []

    for _ in range(cantidad_seleccionados):
        torneo = random.sample(poblacion, k)
        ganador = max(torneo, key=lambda x: x[1][2])  # usamos el fitness
        seleccionados.append(ganador)

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


def fusionar_matrices(matriz_prev, nueva_tabla):
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
        valor_actual = int(matriz_mutada[fila][8])
        opciones = [1, 2, 3, 4]
        opciones.remove(valor_actual)  # evita repetir el mismo valor
        matriz_mutada[fila][8] = np.int64(random.choice(opciones))

    return matriz_mutada




def distancia_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])