import math as math
import random

import numpy as numpy
from typing import List
from SupportFuntions.matrix_operations import inner_product, add_vector, scale_vector, index_of_negative_element, \
    index_of_positive_element, multiply, sub_vector
from Combinatorics.combinations import next_unique_combination
from SystemSolution.solution import is_linear_dependent


class Simplex:
    def __init__(self, matrix: List[list], c: list, x: list, n: List[int], b: List[list]):
        if len(matrix) == 0 or len(matrix[0]) == 0 or len(c) != len(matrix[0]) or len(matrix[0]) != len(x) or \
                len(matrix) != len(b) or len(matrix) != len(b[0]) or len(matrix) != len(n):
            raise ValueError('Parameters dimensions mismatch')
        self._elem_type = type(matrix[0][0])
        if not isinstance(c[0], self._elem_type) or not isinstance(x[0], self._elem_type) or \
                not isinstance(b[0][0], self._elem_type):
            raise ValueError('Params types mismatch!')
        self._a = matrix
        self._c = c
        self._x = x.copy()
        self._b = b
        self._is_optimum = None
        self._n_size = len(self._x)
        self._m_size = len(self._a)
        self._n_k = n.copy()
        self._n_p = [i for i in range(self._n_size) if self._x[i] > 0]
        self._n_0 = [i for i in range(self._n_size) if i not in self._n_p]
        self._l_k = [i for i in range(self._n_size) if i not in self._n_k]

    def get_result(self):
        return self._x.copy()

    def test_result(self):
        if self._is_optimum is None:
            self._is_optimum = self._check_optimum() < 0
        return self._is_optimum

    def _check_optimum(self):
        c_n = [self._c[i] for i in self._n_k]
        c_l = [self._c[i] for i in self._l_k]
        a_l = [[self._a[i][self._l_k[j]] for j in range(len(self._l_k))] for i in range(self._m_size)]
        d_l = sub_vector(c_l, multiply(multiply(c_n, self._b), a_l))
        index = index_of_negative_element(d_l)
        if index >= 0:
            index = self._l_k[index]
        return index

    def _count_u(self, index):
        u = [self._elem_type(0) for _ in range(self._n_size)]
        a_j_k = [self._a[i][index] for i in range(self._m_size)]
        temp = multiply(self._b, a_j_k)
        for i in range(len(self._n_k)):
            u[self._n_k[i]] = temp[i]
        u[index] = self._elem_type(-1)
        return u

    def _next_vector(self, u):
        i_k = self._n_k[index_of_positive_element([u[i] for i in self._n_k])]
        coefficient_k = self._x[i_k] / u[i_k]
        for i in self._n_k:
            if u[i] > 0:
                temp1 = self._x[i] / u[i]
                if temp1 < coefficient_k:
                    i_k = i
                    coefficient_k = temp1
        self._x = sub_vector(self._x, scale_vector(coefficient_k, u))
        return i_k

    def _next_base(self):
        temp1 = [self._n_k[i] for i in range(len(self._n_k)) if self._n_k[i] not in self._n_p]
        i = random.randint(0, len(temp1))
        return temp1[i]

    def _move_next(self, u):
        positive = True
        for i in self._n_k:
            if self._x[i] < 0:
                positive = False
        if positive or index_of_positive_element([u[i] for i in self._n_k if i not in self._n_p]) < 0:
            return self._next_vector(u)
        else:
            return self._next_base()

    def _invert_b(self, i_k_index, j_k):
        a_j_k = [self._a[i][j_k] for i in range(self._m_size)]
        alpha = multiply(self._b, a_j_k)
        f_matrix = [[self._elem_type(0) for _ in range(len(self._n_k))] for _ in range(len(self._n_k))]
        for i in range(len(self._n_k)):
            f_matrix[i][i] = self._elem_type(1)
        for i in range(len(self._n_k)):
            if i == i_k_index:
                f_matrix[i][i_k_index] = 1 / alpha[i_k_index]
            else:
                f_matrix[i][i_k_index] = -alpha[i] / alpha[i_k_index]
        self._b = multiply(f_matrix, self._b)

    def iterate(self):
        j_k = self._check_optimum()
        if j_k < 0:
            self._is_optimum = True
            return
        self._is_optimum = None
        u = self._count_u(j_k)
        if index_of_positive_element(u) < 0:
            self._x = None
            self._is_optimum = True
            return
        i_k = self._move_next(u)
        old_i_k_pos = self._n_k.index(i_k)
        self._n_k[self._n_k.index(i_k)] = j_k
        self._l_k[self._l_k.index(j_k)] = i_k
        self._invert_b(old_i_k_pos, j_k)


def count_params(matrix: List[list], x_0: list):
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
