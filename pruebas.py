import numpy as np

vec1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
vec2 = np.array([4,5,8])

# Encontrar el indice del array que se busca, si existe, sino devuelve -1
print(np.where(vec1 == vec2[0]))  # Devuelve el índice de la primera coincidencia
