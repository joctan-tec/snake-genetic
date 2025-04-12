# Parámetros juego
ANCHO_PANTALLA = 640
ALTO_PANTALLA  = 480
VELOCIDAD = 2
TAMANNO_BLOQUE = 80 # Sirve bien con 20, 40, 80
HAY_INTERFAZ = True  #! Poner en True para ver la interfaz
JUEGO_MANUAL = False  #! Poner en True para jugar manualmente
OBJETIVO_MANZANAS = 10  # Número de manzanas a comer para ganar

# Parámetros algoritmo genetico
CANTIDAD_AGENTES = 50
CANTIDAD_GENERACIONES = 5000
PORCENTAJE_SELECCION = 0.2
TASA_MUTACION = 0.1

# Pesos de cada componente
ALPHA = 100  # score
BETA = 2     # distancia a la manzana
GAMMA = 1    # distancia a la pared
DELTA = 5     # penalización por moverse mucho sin comer
EPSILON = 30  # penalización por morir antes de tiempo