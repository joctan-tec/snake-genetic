from collections import deque
import random

class SnakeLoopDetector:
    def __init__(self, window_size=20, min_repeat=3):
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
        return False

    def _check_pattern(self, pattern_length):
        history_list = list(self.history)
        total_len = len(history_list)

        for i in range(total_len - pattern_length * self.min_repeat + 1):
            pattern = history_list[i:i + pattern_length]
            count = 1
            for j in range(i + pattern_length, total_len - pattern_length + 1, pattern_length):
                if history_list[j:j + pattern_length] == pattern:
                    count += 1
                    if count >= self.min_repeat:
                        return True
                else:
                    break
        return False


