from typing import List
from typing import Callable
from SupportFuntions.matrix_operations import add_vector, scale_vector, chebyshev_norm, inner_product
from SystemSolution.solution import linear_system_solution_llt


class FirstGradientMethodConstStep:
    def __init__(self, dfunc: Callable, step: float, tol: float, x0: List[float]):
        self._df = dfunc
        self._step = step
        self._tol = tol
        self._x0 = x0
        self._x = x0
        self._grad = scale_vector(-1., dfunc(x0))
        self._df_count = 1

    def iterate(self):
        self._x = add_vector(self._x, scale_vector(self._step, self._grad))
        self._grad = scale_vector(-1., self._df(self._x))
        self._df_count += 1

    def test_grad(self):
        return chebyshev_norm(self._grad) < self._tol

    def get_result(self):
        return self._x, self._grad, self._df_count

    def restart(self):
        self._x = self._x0
        self._grad = scale_vector(-1., self._df(self._x0))
        self._df_count = 1

    def set_step(self, new_step: float):
        self._step = new_step

    def set_tolerance(self, new_tol: float):
        self._tol = new_tol

    def set_first_approximation(self, new_x0: List[float]):
        self._x0 = new_x0


class SecondGradientMethodSplittingStep:
    def __init__(self, func: Callable, dfunc: Callable, gesse_func: Callable, split_mul: float,
                 split_tol: float, tol: float, x0: List[float]):
        self._g_f = gesse_func
        self._df = dfunc
        self._f = func
        self._mul = split_mul
        self._delta = split_tol
        self._tol = tol
        self._x0 = x0
        self._x = x0
        self._grad = scale_vector(-1., dfunc(x0))
        self._df_count = 1
        self._f_count = 0
        self._g_f_count = 0

    def iterate(self):
        direction = linear_system_solution_llt(self._g_f(self._x), self._grad)
        self._g_f_count += 1
        step = 1.0
        self._f_count += 2
        f_x_k = self._f(self._x)
        grad_inner_p = self._delta * inner_product(self._grad, direction)
        while (self._f(add_vector(self._x, scale_vector(step, direction))) - f_x_k) > \
                step * grad_inner_p:
            step *= self._mul
        self._x = add_vector(self._x, scale_vector(step, direction))
        self._grad = scale_vector(-1., self._df(self._x))
        self._df_count += 1

    def test_grad(self):
        return chebyshev_norm(self._grad) < self._tol

    def get_result(self):
        return self._x, self._grad, self._df_count, self._f_count, self._g_f_count

    def restart(self):
        self._x = self._x0
        self._grad = scale_vector(-1., self._df(self._x0))
        self._df_count = 1

    def set_tolerance(self, new_tol: float):
        self._tol = new_tol

    def set_first_approximation(self, new_x0: List[float]):
        self._x0 = new_x0
