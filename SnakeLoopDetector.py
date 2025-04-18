from collections import deque
import random

class SnakeLoopDetector:
    def __init__(self, window_size=12, min_repeat=3):
        self.history = deque(maxlen=window_size)
        self.min_repeat = min_repeat

    def update(self, head_pos, direction):
        self.history.append((head_pos, direction))

    def is_looping(self):
        if len(self.history) < self.history.maxlen:
            return False
        
        # Verificar múltiples longitudes de patrón
        for pattern_length in [4, 5, 6]:  # Longitudes comunes de loops
            if self._check_pattern(pattern_length):
                return True
        print(self.history)
        return False

    def _check_pattern(self, pattern_length):
        if len(self.history) < pattern_length * self.min_repeat:
            return False
        
        # Obtener el patrón de referencia (más reciente)
        reference = list(self.history)[-pattern_length:]
        
        # Verificar repeticiones hacia atrás
        for i in range(1, self.min_repeat):
            start = -pattern_length * (i + 1)
            end = -pattern_length * i
            if list(self.history)[start:end] != reference:
                return False
        return True
