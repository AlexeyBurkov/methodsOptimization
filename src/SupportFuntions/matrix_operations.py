from typing import List
import math


def inner_product(x: list, y: list):
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Dimension mismatch!")
    if not isinstance(x[0], type(y[0])):
        raise ValueError("Type mismatch!")
    res = x[0] * y[0]
    for i in range(1, len(x)):
        res += x[i] * y[i]
    return res


def euclid_norm(x: list):
    return math.sqrt(inner_product(x, x))


def chebyshev_norm(x: list):
    return abs(max(x, key=abs))


def add_vector(x: list, y: list):
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Dimension mismatch!")
    if not isinstance(x[0], type(y[0])):
        raise ValueError("Type mismatch!")
    return [x[i] + y[i] for i in range(len(x))]


def scale_vector(a, x: list):
    if not isinstance(a, type(x[0])):
        raise ValueError("Type mismatch!")
    return [a * i for i in x]


def index_of_negative_element(x: list):
    for i in range(len(x)):
        if x[i] < 0:
            return i
    return -1


def index_of_positive_element(x: list):
    for i in range(len(x)):
        if x[i] > 0:
            return i
    return -1


def decomposition_llt(matrix: List[list]):
    if len(matrix) == 0 or len(matrix) != len(matrix[0]):
        raise ValueError("Dimension error!")
    result = [matrix[i].copy() for i in range(len(matrix))]
    for i in range(len(matrix[0])):
        temp = matrix[i][i]
        for j in range(i):
            temp -= result[i][j] * result[i][j]
        temp = math.sqrt(temp)
        result[i][i] = temp
        for j in range(i + 1, len(matrix)):
            result[j][i] = matrix[j][i]
            for k in range(i):
                result[j][i] -= result[i][k] * result[j][k]
            result[j][i] /= temp
            result[i][j] = result[j][i]
    return result
