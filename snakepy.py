# Código descargado de https://github.com/patrickloeber/snake-ai-pytorch/blob/main/snake_game_human.py

import random
from collections import namedtuple
from enum import Enum
import pprint

import pygame
import constantes as const
from func_geneticos import fitness, distancia_manhattan
import numpy as np
import time

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

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.individuo = []
        self.filas = const.ALTO_PANTALLA // const.TAMANNO_BLOQUE
        self.columnas = const.ANCHO_PANTALLA // const.TAMANNO_BLOQUE
        # init display

        if(const.HAY_INTERFAZ):
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step_automatico(self):
        # 1. collect user input
        
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
        elif numero_aleatorio < 100:
            if self.direction != Direction.UP:
                self.direction = Direction.DOWN


        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

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
        print(f"cabeza {cabeza} - manzana {manzana} - distancia_manhattan {distancia_manzana}")

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
        self.snake.insert(0, self.head)

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
        print(f"cabeza {cabeza} - manzana {manzana} - distancia_manhattan {distancia_manzana}")

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

def jugar(num_individuo):

    game = SnakeGame(const.ANCHO_PANTALLA, const.ALTO_PANTALLA)

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
    # Retornar resultados
    resultados = {
        "individuo": individuo,
        "duracion": end - start,
        "fitness": fitness(individuo)
    }
    
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
    print(jugar(1))