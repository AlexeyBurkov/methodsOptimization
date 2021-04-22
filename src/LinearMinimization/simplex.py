import math as math
import random

import numpy as numpy
from fractions import Fraction as Q
from typing import List
from SupportFuntions.matrix_operations import inner_product, add_vector, scale_vector, index_of_negative_element, \
    index_of_positive_element, multiply, sub_vector
from Combinatorics.combinations import next_unique_combination
from SystemSolution.solution import is_linear_dependent


def count_params(matrix: List[List[Q]], x_0: List[Q]):
    n_p = [i for i in range(len(x_0)) if x_0[i] > 0]
    n_0 = [i for i in range(len(x_0)) if i not in n_p]
    n_k = n_p.copy()
    max_val = len(n_0)
    combination = [i for i in range(len(matrix) - len(n_p))]
    while len(combination):
        found = True
        for i in combination:
            if not is_linear_dependent(matrix, n_k, n_0[i]):
                n_k.append(n_0[i])
            else:
                n_k = n_p.copy()
                combination = next_unique_combination(combination, max_val)
                found = False
                break
        if found:
            combination = []
    return n_k[:len(matrix)]


def simplex(a_matrix: List[List[Q]], c_vec: List[Q], x_0: List[Q], n_k: List[int], b_matrix: List[List[Q]]):
    n_size = len(x_0)
    m_size = len(a_matrix)
    n_p = [i for i in range(n_size) if x_0[i] > 0]
    n_0 = [i for i in range(n_size) if i not in n_p]
    l_k = [i for i in range(n_size) if i not in n_k]
    while True:
        c_n = [c_vec[i] for i in n_k]
        c_l = [c_vec[i] for i in l_k]
        a_l = [[a_matrix[i][l_k[j]] for j in range(len(l_k))] for i in range(m_size)]
        d_l = sub_vector(c_l, multiply(multiply(c_n, b_matrix), a_l))
        #
        j_k = index_of_negative_element(d_l)
        if j_k < 0:
            return x_0
        j_k = l_k[j_k]
        #
        u_k = [Q(0) for _ in range(n_size)]
        a_j_k = [a_matrix[i][j_k] for i in range(m_size)]
        temp = multiply(b_matrix, a_j_k)
        for i in range(len(n_k)):
            u_k[n_k[i]] = temp[i]
        u_k[j_k] = Q(-1)
        #
        if index_of_positive_element(u_k) < 0:
            return None
        #
        i_k = 0
        positive = True
        for i in n_k:
            if x_0[i] < 0:
                positive = False
        if positive or index_of_positive_element([u_k[i] for i in n_k if i not in n_p]) < 0:
            i_k = n_k[index_of_positive_element([u_k[i] for i in n_k])]
            coefficient_k = x_0[i_k] / u_k[i_k]
            for i in n_k:
                if u_k[i] > 0:
                    temp1 = x_0[i] / u_k[i]
                    if temp1 < coefficient_k:
                        i_k = i
                        coefficient_k = temp1
            x_0 = add_vector(x_0, scale_vector(-coefficient_k, u_k))
            print(x_0)
        else:
            temp1 = [n_k[i] for i in range(len(n_k)) if n_k[i] not in n_p]
            i = random.randint(0, len(temp1))
            i_k = temp1[i]
        j = n_k.index(i_k)
        n_k[n_k.index(i_k)] = j_k
        l_k[l_k.index(j_k)] = i_k
        a_j_k = [a_matrix[i][j_k] for i in range(m_size)]
        alpha = multiply(b_matrix, a_j_k)
        f_matrix = [[Q(0) for _ in range(len(n_k))] for _ in range(len(n_k))]
        for i in range(len(n_k)):
            f_matrix[i][i] = Q(1)
        for i in range(len(n_k)):
            if i == j:
                f_matrix[i][j] = 1 / alpha[j]
            else:
                f_matrix[i][j] = -alpha[i] / alpha[j]
        b_matrix = multiply(f_matrix, b_matrix)
