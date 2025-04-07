from multiprocessing import Pool
import constantes as const
from snakepy import jugar


def jugar_con_resultado(indice):
    # Asumimos que `jugar(indice)` retorna un diccionario con 'individuo', 'duracion' y 'fitness'
    return (indice, jugar(indice))


def main():
    print("Iniciando los procesos del juego...")

    with Pool(processes=const.CANTIDAD_AGENTES) as pool:
        resultados = pool.map(jugar_con_resultado, range(const.CANTIDAD_AGENTES))

    print("Todos los procesos han terminado.")

    # Procesar los resultados
    for indice, resultado in resultados:
        print(f"Agente {indice}:")
        print(f"  Individuo: {resultado['individuo']}")
        print(f"  Duración: {resultado['duracion']}")
        print(f"  Fitness: {resultado['fitness']}")


if __name__ == "__main__":
    main()
