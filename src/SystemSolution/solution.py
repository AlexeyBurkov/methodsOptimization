from typing import List
from SupportFuntions.matrix_operations import decomposition_llt


def linear_system_solution_llt(matrix: List[list], vector: list):
    if len(matrix) == 0 or len(matrix) != len(matrix[0]) or len(matrix) != len(vector):
        raise ValueError("Dimension error!")
    temp_m = decomposition_llt(matrix)
    temp_v = vector.copy()
    for i in range(len(vector)):
        temp = vector[i]
        for j in range(i):
            temp -= temp_v[j] * temp_m[i][j]
        temp_v[i] = temp / temp_m[i][i]
    result = temp_v.copy()
    for i in range(len(vector) - 1, -1, -1):
        temp = temp_v[i]
        for j in range(len(vector) - 1, i, -1):
            temp -= result[j] * temp_m[i][j]
        result[i] = temp / temp_m[i][i]
    return result
