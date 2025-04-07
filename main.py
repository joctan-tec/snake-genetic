import threading
import constantes as const
from snakepy import jugar


def main():
    # Iniciar los hilos del juego
    hilos = []
    resultados = [None] * const.CANTIDAD_AGENTES

    def jugar_con_resultado(indice):
        resultados[indice] = jugar()

    for i in range(const.CANTIDAD_AGENTES):
        hilo = threading.Thread(target=jugar_con_resultado, args=(i,))
        hilos.append(hilo)
        hilo.start()
    print("Iniciando los hilos del juego...")

    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    print("Todos los hilos han terminado.")
    # Procesar los resultados
    for i, resultado in enumerate(resultados):
        print(f"Agente {i}:")
        print(f"  Individuo: {resultado['individuo']}")
        print(f"  Duración: {resultado['duracion']}")
        print(f"  Fitness: {resultado['fitness']}")


if __name__ == "__main__": 
    main()