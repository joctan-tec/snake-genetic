# Código descargado de https://github.com/patrickloeber/snake-ai-pytorch/blob/main/snake_game_human.py

import random
from collections import namedtuple
from enum import Enum
from custom_utils import mostrar_tabla
import pandas as pd





import pygame
import constantes as const
from func_geneticos import fitness, distancia_manhattan, leer_matriz
import numpy as np
import time
from SnakeLoopDetector import SnakeLoopDetector

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()
# font = pygame.font.Font("arial.ttf", 25)
font = pygame.font.SysFont("arial", 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE =  const.TAMANNO_BLOQUE
SPEED = const.VELOCIDAD

class SnakeGame:

    def __init__(self, matriz_decisiones, juego_id, w=640, h=480):
        self.w = w
        self.h = h
        self.individuo = []
        self.filas = const.ALTO_PANTALLA // const.TAMANNO_BLOQUE
        self.columnas = const.ANCHO_PANTALLA // const.TAMANNO_BLOQUE
        self.matriz_decisiones = matriz_decisiones
        self.loop_detector = SnakeLoopDetector()
        self.juego_id = juego_id
        self.posiciones_manzanas = [
            Point(2 * const.TAMANNO_BLOQUE, 4 * const.TAMANNO_BLOQUE),
            Point(1 * const.TAMANNO_BLOQUE, 2 * const.TAMANNO_BLOQUE),
            Point(3 * const.TAMANNO_BLOQUE, 1 * const.TAMANNO_BLOQUE),
            Point(4 * const.TAMANNO_BLOQUE, 4 * const.TAMANNO_BLOQUE),
        ]
        self.manzana_usada = 0
        self.fitness = 0

        # init display

        if(const.HAY_INTERFAZ):
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        if(const.NO_CUERPO):
            self.snake = [self.head]
        else:
            self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
            ]

        self.score = 0
        self.food = None
        self._place_food()

    def __manzana_en_direcciones(self):
        # Devuelve una lista de booleanos en el orden: [izquierda, derecha, arriba, abajo]
        resultado = []

        # IZQUIERDA
        hay_manzana = False
        for i in range(1, self.columnas):
            if self.food == Point(self.head.x - (i * BLOCK_SIZE), self.head.y):
                hay_manzana = True
                break
        resultado.append(hay_manzana)

        # DERECHA
        hay_manzana = False
        for i in range(1, self.columnas):
            if self.food == Point(self.head.x + (i * BLOCK_SIZE), self.head.y):
                hay_manzana = True
                break
        resultado.append(hay_manzana)

        # ARRIBA
        hay_manzana = False
        for i in range(1, self.filas):
            if self.food == Point(self.head.x, self.head.y - (i * BLOCK_SIZE)):
                hay_manzana = True
                break
        resultado.append(hay_manzana)

        # ABAJO
        hay_manzana = False
        for i in range(1, self.filas):
            if self.food == Point(self.head.x, self.head.y + (i * BLOCK_SIZE)):
                hay_manzana = True
                break
        resultado.append(hay_manzana)

        return resultado



    def _place_food(self):
        # Si const.MANZANAS_FIJAS es True, la comida saldrá en posiciones fijas
        # Si no, la comida saldrá en posiciones aleatorias
        if const.MANZANAS_FIJAS:
            
            if self.manzana_usada >= len(self.posiciones_manzanas):
                self.manzana_usada = 0
            self.food = self.posiciones_manzanas[self.manzana_usada]
            self.manzana_usada += 1
            
        else:
            x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food = Point(x, y)
            if self.food in self.snake:
                self._place_food()

    def play_step_automatico(self):
        # 1. Obtener posición y dirección actual
        head_columna, head_fila = (int(self.head.x), int(self.head.y))
        head_columna = head_columna // const.TAMANNO_BLOQUE
        head_fila = head_fila // const.TAMANNO_BLOQUE
        direccion_antes = self.direction
        cabeza_antes = (head_fila, head_columna)

        # 2. Calcular distancia a la manzana y distancia a la pared en la dirección actual
        manzana = (int(self.food.y) // const.TAMANNO_BLOQUE, int(self.food.x) // const.TAMANNO_BLOQUE)
        cabeza = (head_fila, head_columna)

        match self.direction:
            case Direction.RIGHT:
                distancia_pared = self.columnas - head_columna - 1
            case Direction.LEFT:
                distancia_pared = head_columna
            case Direction.UP:
                distancia_pared = head_fila
            case Direction.DOWN:
                distancia_pared = self.filas - head_fila - 1

        distancia_manzana = distancia_manhattan(cabeza, manzana)

        # 3. Buscar coincidencia en matriz_decisiones
        estado_actual = np.array([head_fila, head_columna, self.direction.value, manzana[0], manzana[1], distancia_manzana, distancia_pared])
        coincidencia = None
        # Si la matriz_decisiones está vacía, no se puede buscar coincidencias
        if self.matriz_decisiones.size != 0:
            
            matriz = self.matriz_decisiones[:, :7]  # extrae solo los primeros 7 elementos de cada fila
            coincidencias = np.all(matriz == estado_actual, axis=1)  # compara con estado_actual

            if np.any(coincidencias):
                coincidencia = self.matriz_decisiones[coincidencias][0]  # toma la primera coincidencia
            


        # 4. Detectar loop y decidir dirección
        self.loop_detector.update(cabeza, self.direction)
        hay_loop = self.loop_detector.is_looping()

        if hay_loop:
            if const.HAY_INTERFAZ:
                print("¡Loop detectado! Movimiento aleatorio forzado.")
            direcciones = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            direcciones = [d for d in direcciones if not (
                (d == Direction.LEFT and self.direction == Direction.RIGHT) or
                (d == Direction.RIGHT and self.direction == Direction.LEFT) or
                (d == Direction.UP and self.direction == Direction.DOWN) or
                (d == Direction.DOWN and self.direction == Direction.UP)
            )]
            self.direction = random.choice(direcciones)
        elif coincidencia is not None:
            direccion_elegida_valor = int(coincidencia[8])
            # Validar que no se devuelva
            if (direccion_elegida_valor == 1 and self.direction == Direction.LEFT) or (direccion_elegida_valor == 2 and self.direction == Direction.RIGHT) or (direccion_elegida_valor == 3 and self.direction == Direction.DOWN) or (direccion_elegida_valor == 4 and self.direction == Direction.UP):
                pass  # Mantener dirección actual
            else:
                self.direction = Direction(direccion_elegida_valor)
            if const.HAY_INTERFAZ:
                print("Encontré coincidencia en la tabla")
        else:
            numero_aleatorio = random.randint(0, 100)
            if numero_aleatorio < 25:
                if self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
            elif numero_aleatorio < 50:
                if self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
            elif numero_aleatorio < 75:
                if self.direction != Direction.DOWN:
                    self.direction = Direction.UP
            else:
                if self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # 5. Mover
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)
        cabeza = (int(self.head.y) // const.TAMANNO_BLOQUE, int(self.head.x) // const.TAMANNO_BLOQUE)

        # 6. Revisar colisión
        game_over = False
        if self._is_collision(): 
            game_over = True
            self.fitness -= 10 
            

        # 7. Comida
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self.fitness += 10
            if const.NO_CUERPO:
                self.snake.pop()  # No permitimos que crezca, quitamos la cola como si no hubiera comido
        else:
            self.snake.pop()
            self.fitness -= 0.1  # Penaliza por no comer

        # 8. Registrar cromosoma 
        """
            Significado de cromosoma:
            [
                fila cabeza,
                columna cabeza,
                direccion antes,
                fila manzana,
                columna manzana,
                distancia manzana,
                distancia pared,
                score,
                direccion después (accion tomada)
            ]
        """
        distancia_manzana_actual = distancia_manhattan(cabeza, manzana)

        # Si la distancia se reduce, se considera que la acción fue correcta
        if distancia_manzana_actual < distancia_manzana:
            cromosoma = [cabeza_antes[0], cabeza_antes[1], direccion_antes.value, manzana[0], manzana[1], distancia_manzana, distancia_pared, self.score, self.direction.value]
            self.individuo.append(cromosoma)
        # print(f"{self.juego_id} : " ,cromosoma)

        # 9. Actualizar UI y reloj
        if const.HAY_INTERFAZ:
            self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score



    def play_step_manual(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

    
        # 2. move
        self._move(self.direction)  # update the head
        #self.snake.insert(0, self.head)

        head_columna, head_fila = (int(self.head.x), int(self.head.y))
        head_columna = head_columna // const.TAMANNO_BLOQUE
        head_fila = head_fila // const.TAMANNO_BLOQUE
        direccion = self.direction
        # (fila, columna)
        cabeza = (head_fila, head_columna)
        manzana = (int(self.food.y) // const.TAMANNO_BLOQUE, int(self.food.x) // const.TAMANNO_BLOQUE)

        # Obtener distancia a la pared de la dirección de la cabeza
        match direccion:
            case Direction.RIGHT:
                distancia_pared = self.columnas - head_columna - 1
            case Direction.LEFT:
                distancia_pared = head_columna
            case Direction.UP:
                distancia_pared = head_fila
            case Direction.DOWN:
                distancia_pared = self.filas - head_fila - 1
        
        
        # Obtiene la distancia a la manzana pero utiliza la distancia tomando en cuenta el cuadrado completo
        distancia_manzana = distancia_manhattan(cabeza, manzana)
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. Se agrega el score actualizado
        cromosoma = [distancia_manzana, distancia_pared, self.score, direccion.value]
        self.individuo.append(cromosoma)

        # 5. update ui and clock
        if(const.HAY_INTERFAZ):
            self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if (
            self.head.x > self.w - BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.h - BLOCK_SIZE
            or self.head.y < 0
        ):
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):

        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(
            self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE)
        )

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

def jugar(num_individuo, matriz_decisiones):
    game = SnakeGame(matriz_decisiones, num_individuo, const.ANCHO_PANTALLA, const.ALTO_PANTALLA)

    start = time.time()

    # game loop
    while True:
        if(const.JUEGO_MANUAL):
            game_over, score = game.play_step_manual()
        else:
            game_over, score = game.play_step_automatico()

        if game_over == True:
            end = time.time()
            break

    individuo = np.array(game.individuo, dtype=int)
    
    """ df = pd.DataFrame(individuo, columns=["columna", "fila", "direccion antes", "distancia manzana", "manzana izquierda", "manzana derecha", "manzana arriba", "manzana abajo", "distancia pared", "score", "direccion después"])
    
    mostrar_tabla(df) """
    
    # Verificar si la matriz viene vacia
    if individuo.size == 0:
        #print("El individuo está vacío")
        return None
    resultados = [individuo, end - start, game.fitness]
    
    # print(f"Agente {num_individuo} terminó el juego")
    pygame.quit()
    return resultados



'''
[ distancia_manzana, distancia_pared, score, accion ]
'''

'''
[ distancia_manzana
  distancia_pared 
  score
  direccion 
  accion ]
'''


if __name__ == "__main__":
    print("Iniciando juego...")
    try: 
        matriz_decisiones = leer_matriz()
    except Exception as e:
        print(f"Error al leer la matriz: {e}")
        matriz_decisiones = np.array([])
    print(jugar(1, matriz_decisiones))
    