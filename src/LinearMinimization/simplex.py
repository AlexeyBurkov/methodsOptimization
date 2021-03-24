import math as math
from fractions import Fraction as Q
from typing import List
from SupportFuntions.matrix_operations import inner_product, add_vector, scale_vector, index_of_negative_element, \
    index_of_positive_element


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
    elif type(a[0]) is Q:
        if type(b[0]) is list:
            if len(a) != len(b[0]):
                raise ValueError("Dimension mismatch!")
            if type(b[0][0]) is not Q:
                raise ValueError("Invalid matrix element type!")
            res = [Q(0) for _ in range(len(b[0]))]
            for i in range(len(b[0])):
                for k in range(len(a)):
                    res[i] += a[i] * b[k][i]
            return res
        else:
            raise ValueError("Invalid arguments types!")
    else:
        raise ValueError("Invalid arguments types!")


def transpose(matrix: List[List[Q]]):
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


def gaussian_elimination(matrix: List[List[Q]], vector: List[Q]):
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


def is_linear_dependent(vector_list: List[List[Q]], indexes: List[int], index: int):
    new_vector = vector_list[index].copy()
    vector_size = len(new_vector)
    for j in indexes:
        coefficient = inner_product(new_vector, vector_list[j]) / euclid_norm(vector_list[j])
        for k in range(vector_size):
            new_vector[k] -= coefficient * vector_list[j][k]
    return chebyshev_norm(new_vector) == 0


def next_unique_combination(x: List[int], max_value: int):
    for i in range(len(x) - 1, -1, -1):
        if x[i] < (max_value - len(x) + 1 + i):
            x[i] += 1
            for j in range(i + 1, len(x)):
                x[j] = x[j - 1] + 1
                if x[j] > max_value:
                    x.clear()
                    break
            return x
    x.clear()
    return x


def count_params(matrix: List[List[Q]], x_0: List[Q]):
    n_p = [i for i in range(len(x_0)) if x_0[i] > 0]
    n_0 = [i for i in range(len(x_0)) if x_0[i] == 0]
    n_k = n_p.copy()
    max_val = len(n_0)
    combination = [i for i in range(len(matrix) - len(n_p))]
    found = True
    while len(combination):
        for i in combination:
            if not is_linear_dependent(matrix, n_k, n_0[i]):
                n_k.append(n_0[i])
            else:
                n_k = n_p.copy()
                combination = next_unique_combination(combination, max_val)
                found = False
        if found:
            combination = []
    return n_k[:len(matrix)]


def simplex(a_matrix: List[List[Q]], c_vec: List[Q], x_0: List[Q], n_k: List[int], b_matrix: List[List[Q]]):
    n_size = len(x_0)
    m_size = len(a_matrix)
    n_p = [i for i in range(n_size) if x_0[i] > 0]
    l_k = [i for i in range(n_size) if i not in n_k]
    while True:
        c_n = [c_vec[i] for i in n_k]
        c_l = [c_vec[i] for i in l_k]
        a_l = [[a_matrix[i][l_k[j]] for j in range(m_size) if j in range(len(l_k))] for i in range(m_size)]
        d_l = add_vector(c_l, scale_vector(-1, multiply(multiply(c_n, b_matrix), a_l)))
        j_k = index_of_negative_element(d_l)
        if j_k < 0:
            return x_0
        u_k = [Q(0) for _ in range(n_size)]
        a_j_k = [a_matrix[i][j_k] for i in range(m_size)]
        temp = multiply(b_matrix, a_j_k)
        for i in range(len(n_k)):
            u_k[n_k[i]] = temp[i]
        u_k[j_k] = Q(-1)
        if index_of_positive_element(u_k) >= 0:
            return None
        if n_k == n_p or index_of_positive_element([u_k[i] for i in n_k if i not in n_p]) < 0:
            coefficient_k = min([x_0[i] / u_k[i] for i in range(n_size) if u_k[i] > 0])
            x_0 = add_vector(x_0, scale_vector(-coefficient_k, u_k))
        else:


# def solve_simplex(a_matrix, b_vec, c_vec, x_0_vec):
#     n_k = count_params(a_matrix, x_0_vec)
#     b_matrix =


if __name__ == "__main__":
