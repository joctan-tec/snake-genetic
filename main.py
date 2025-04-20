from multiprocessing import Pool
import constantes as const
from snakepy import jugar
from func_geneticos import seleccion_por_ranking, cruce_concatenado,cruce, guardar_matriz, leer_matriz, fusionar_matrices, mutar_movimientos
import numpy as np
import matplotlib.pyplot as plt
import time

FITNESS_PROMEDIO_GENERACION = []
MEJOR_FITNESS_GENERACION = []

FITNESS_PROMEDIO_SELECCION = []
MEJOR_FITNESS_SELECCION = []


def jugar_con_resultado(args):
    indice, matriz_decisiones = args
    # Asumimos que `jugar(indice)` retorna un diccionario con 'individuo', 'duracion' y 'fitness'
    return [indice, jugar(indice, matriz_decisiones)]




def main():
    start = time.time()
    try:
        matriz_decisiones = leer_matriz()
    except:
        matriz_decisiones = np.array([])

    with Pool(processes=const.CANTIDAD_AGENTES) as pool:
        for i in range(const.CANTIDAD_GENERACIONES):
            print(f'======================= GENERACIÓN {i+1} ==========================')
            print("Iniciando los procesos del juego...")
            
            argumentos = [[i, matriz_decisiones] for i in range(const.CANTIDAD_AGENTES)]  # Crear lista de tuplas
            # resultados_juego = pool.map(jugar_con_resultado, argumentos)
            resultados = pool.map(jugar_con_resultado, argumentos)

            # resultados = []
            # for i, resultado in enumerate(resultados_juego):
            #     if not np.array_equal(resultado[1][0], []):
            #         resultados.append(resultado)

            print("Todos los procesos han terminado.")
            print(f'======================= ESTADISTICAS ===========================')

            # Paso 1: Ordenar por fitness (mayor es mejor en maximización)
            ordenados = sorted(resultados, key=lambda x: x[1][2], reverse=True)
            mejor_fitness = ordenados[0][1][2]
            MEJOR_FITNESS_GENERACION.append(mejor_fitness)
            
            # Paso 2: Asignar probabilidades basadas en el ranking (más alto, más probabilidad)
            N = len(ordenados)
            ranking_probabilidades = [(N - i) / sum(range(1, N + 1)) for i in range(N)]
            fitness_promedio = sum([x[1][2] for x in ordenados]) / N
            FITNESS_PROMEDIO_GENERACION.append(fitness_promedio)

            print(f'Mejor fitness de esta generación: {float(mejor_fitness)}')
            print(f'Fitness promedio de esta generación: {float(fitness_promedio)}')



            # Paso 3: Seleccionar k individuos
            # Ejemplo: seleccionar 2 padres
            k=int(N*const.PORCENTAJE_SELECCION)
            # padres = seleccion_por_ranking(ordenados, ranking_probabilidades, k)
            # padres = sorted(padres, key=lambda x: x[1][2], reverse=True)
            padres = ordenados[:k]
            mejor_fitness_seleccion = padres[0][1][2]
            fitness_promedio_seleccion = sum([x[1][2] for x in padres]) / k
            MEJOR_FITNESS_SELECCION.append(mejor_fitness_seleccion)
            FITNESS_PROMEDIO_SELECCION.append(fitness_promedio_seleccion)
            
            print(f'Mejor fitness de la selección: {float(mejor_fitness_seleccion)}')
            print(f'Fitness promedio de la selección: {float(fitness_promedio_seleccion)}')

            print(f'================================================================\n')

            # Generar un único hijo a partir de todos los padresd
            nueva_tabla = cruce(padres)
            # nueva_tabla = cruce_concatenado(padres)
            # Mutar el hijo
            tabla_mutada = mutar_movimientos(nueva_tabla.copy(), tasa_mutacion=const.TASA_MUTACION)
            # Fusionar con el hijo mutado y sin mutar
            tabla_fusionada = fusionar_matrices(matriz_decisiones, tabla_mutada)
            matriz_decisiones = fusionar_matrices(tabla_fusionada, nueva_tabla)

            # Guardar la nueva matriz mutada
            guardar_matriz(matriz_decisiones)

    end = time.time()
    print(f"Tiempo total de ejecución: {end - start} segundos")
    print(leer_matriz())
    print(leer_matriz().shape)

    # Graficar resultados
    plt.plot(FITNESS_PROMEDIO_GENERACION, label='Promedio Generación')
    # plt.plot(MEJOR_FITNESS_GENERACION, label='Mejor Generación')
    # plt.plot(FITNESS_PROMEDIO_SELECCION, label='Promedio Selección')
    plt.plot(MEJOR_FITNESS_SELECCION, label='Mejor Selección')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del Fitness')
    plt.legend()
    plt.grid()
    plt.show()


    


    


if __name__ == "__main__":
    main()
