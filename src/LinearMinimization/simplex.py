import math as math
from fractions import Fraction as Q
from typing import List
from SupportFuntions.matrix_operations import inner_product, add_vector, scale_vector, index_of_negative_element, \
    index_of_positive_element, multiply, is_linear_dependent
from Combinatorics.combinations import next_unique_combination


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