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


def transpose(matrix: List[list]):
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


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


def multiply(a: list, b: list):
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Invalid argument dimensions!")
    if type(a[0]) is list:
        if type(b[0]) is list:
            if len(a) != len(b[0]) or len(a[0]) != len(b):
                raise ValueError("Dimension mismatch!")
            if not isinstance(a[0][0], type(b[0][0])):
                raise ValueError("Invalid matrix element type!")
            res = [[a[i][0] * b[0][j] for j in range(len(b))] for i in range(len(a))]
            for i in range(len(a)):
                for j in range(len(b)):
                    for k in range(1, len(b)):
                        res[i][j] += a[i][k] * b[k][j]
            return res
        elif isinstance(b[0], type(a[0][0])):
            return [inner_product(a[i], b) for i in range(len(a))]
        else:
            raise ValueError("Invalid vector element type!")
    elif type(b[0]) is list:
        if len(a) != len(b[0]):
            raise ValueError("Dimension mismatch!")
        if not isinstance(a[0], type(b[0][0])):
            raise ValueError("Invalid matrix element type!")
        res = [a[i] * b[0][i] for i in range(len(b[0]))]
        for i in range(len(b[0])):
            for k in range(1, len(a)):
                res[i] += a[i] * b[k][i]
        return res
    else:
        raise ValueError("Invalid arguments types!")


def gaussian_elimination(matrix: List[list], vector: list):
    if len(matrix) != len(vector) or len(vector) == 0:
        raise ValueError("Dimension mismatch!")
    current_i = 0
    for i in range(len(matrix[0])):
        main_element = matrix[current_i + i][i]
        while main_element == 0:
            for j in range(i + 1, len(matrix)):
                if matrix[current_i + j][i] != 0:
                    main_element = matrix[current_i + j][i]
                    for k in range(len(matrix[0])):
                        temp = matrix[current_i + j][k]
                        matrix[current_i + j][k] = matrix[current_i + i][k]
                        matrix[current_i + i][k] = temp
                    break
            if main_element == 0:
                current_i -= 1
                i += 1
                if i == len(matrix[0]):
                    break
        if main_element != 0:
            for j in range(current_i)


def is_linear_dependent(vector_list: List[list], indexes: List[int], index: int):

