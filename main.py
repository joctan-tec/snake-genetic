from multiprocessing import Pool, TimeoutError
from copy import deepcopy
import constantes as const
from snakepy import jugar
from func_geneticos import seleccion_por_ranking, cruce_concatenado, guardar_matriz, leer_matriz, fusionar_matrices, mutar_movimientos, seleccion_torneo
import numpy as np
import matplotlib.pyplot as plt

FITNESS_PROMEDIO_GENERACION = []
MEJOR_FITNESS_GENERACION = []



SCORE_PROMEDIO_GENERACION = []
MEJOR_SCORE_GENERACION = []


def jugar_con_resultado(args):
    agente_id, matriz_decisiones = args
    
    try:
        resultado = jugar(agente_id, matriz_decisiones)
        return (agente_id, resultado)
    except Exception as e:
        print(f"[Agente {agente_id}] Error: {e}")
        return (agente_id, None)

def main():
    print("Creando pool de procesos...\n")
    
    with Pool(processes=const.CANTIDAD_AGENTES) as pool:
        for i in range(const.CANTIDAD_GENERACIONES):
            print(f'======================= GENERACIÓN {i+1} ==========================')
            print("Iniciando los procesos del juego...")

            try:
                matriz_decisiones = leer_matriz()
            except Exception as e:
                print(f"Error al leer la matriz: {e}")
                matriz_decisiones = np.array([])

            argumentos = [(j, deepcopy(matriz_decisiones)) for j in range(const.CANTIDAD_AGENTES)]
            async_results = [pool.apply_async(jugar_con_resultado, args=(arg,)) for arg in argumentos]
            resultados = []

            for j, r in enumerate(async_results):
                try:
                    resultado = r.get(timeout=15)
                    resultados.append(resultado)
                except TimeoutError:
                    print(f"[Agente {j}] ❌ Proceso se demoró demasiado y fue descartado.")
                    resultados.append((j, None))
            print("Todos los procesos han terminado.")
            print(f'======================= ESTADISTICAS ===========================')

            # Asegurarte de filtrar resultados nulos
            resultados_validos = [r for r in resultados if r[1] is not None]
            if not resultados_validos:
                print("⚠️ No hubo resultados válidos. Saltando generación.")
                continue

            ordenados = sorted(resultados_validos, key=lambda x: x[1][2], reverse=True)
            mejor_fitness = ordenados[0][1][2]
            MEJOR_FITNESS_GENERACION.append(mejor_fitness)

            N = len(ordenados)
            ranking_probabilidades = [(N - i) / sum(range(1, N + 1)) for i in range(N)]
            fitness_promedio = sum([x[1][2] for x in ordenados]) / N
            FITNESS_PROMEDIO_GENERACION.append(fitness_promedio)

            todos_los_scores = [movimiento[7] for individuo in ordenados for movimiento in individuo[1][0]]
            score_promedio = sum(todos_los_scores) / len(todos_los_scores)
            mejor_score = max(todos_los_scores)

            SCORE_PROMEDIO_GENERACION.append(score_promedio)
            MEJOR_SCORE_GENERACION.append(mejor_score)


            print(f'Mejor fitness de esta generación: {float(mejor_fitness)}')
            print(f'Fitness promedio de esta generación: {float(fitness_promedio)}')

            print(f'Score promedio de esta generación: {float(score_promedio)}')
            print(f'Mejor score de esta generación: {float(mejor_score)}')

            # Selección
            k = int(N * const.PORCENTAJE_SELECCION)
            padres = seleccion_torneo(ordenados, cantidad_seleccionados=k)
            padres = sorted(padres, key=lambda x: x[1][2], reverse=True)

            # Cruce y mutación
            nueva_tabla = cruce_concatenado(padres)
            tabla_fusionada = fusionar_matrices(matriz_decisiones, nueva_tabla)
            matriz_final = mutar_movimientos(tabla_fusionada, tasa_mutacion=const.TASA_MUTACION)

            guardar_matriz(matriz_final)

    print("Ejecución finalizada. Leyendo matriz final...\n")
    print(leer_matriz())
    print(leer_matriz().shape)

    mejor_individuo = max([x[5] for x in matriz_decisiones])
    print(f"Mejor individuo: {mejor_individuo}")

    # Graficar resultados en dos subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    # Gráfico de Fitness
    axs[0].plot(FITNESS_PROMEDIO_GENERACION, label='Fitness Promedio', color='blue')
    axs[0].plot(MEJOR_FITNESS_GENERACION, label='Mejor Fitness', color='orange')
    axs[0].set_xlabel('Generación')
    axs[0].set_ylabel('Fitness')
    axs[0].set_title('Evolución del Fitness')
    axs[0].legend()
    axs[0].grid(True)

    # Gráfico de Score
    axs[1].plot(SCORE_PROMEDIO_GENERACION, label='Score Promedio', color='green')
    axs[1].plot(MEJOR_SCORE_GENERACION, label='Mejor Score', color='red')
    axs[1].set_xlabel('Generación')
    axs[1].set_ylabel('Score')
    axs[1].set_title('Evolución del Score')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig("grafica.png", dpi=300, bbox_inches='tight')
    plt.show()


    


    


if __name__ == "__main__":
    main()
