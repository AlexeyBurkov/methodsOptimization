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


def linear_system_solution_gaussian_elimination(matrix: List[list], vector: list):
    if len(matrix) != len(vector) or len(vector) == 0:
        raise ValueError("Dimension mismatch!")
    m = [a.copy() for a in matrix]
    current_i = 0
    for i in range(len(m[0])):
        main_element = m[current_i + i][i]
        while main_element == 0:
            for j in range(i + 1, len(m)):
                if m[current_i + j][i] != 0:
                    main_element = m[current_i + j][i]
                    for k in range(len(m[0])):
                        temp = m[current_i + j][k]
                        m[current_i + j][k] = m[current_i + i][k]
                        m[current_i + i][k] = temp
                    break
            if main_element == 0:
                current_i -= 1
                i += 1
                if i == len(m[0]):
                    break
        if main_element != 0:
            for j in range(current_i + i + 1, len(m)):
                if m[j][i] != 0:
                    mul = m[j][i] / main_element
                    for k in range(i, len(m[j])):
                        m[j][k] -= mul * m[current_i + i][k]

