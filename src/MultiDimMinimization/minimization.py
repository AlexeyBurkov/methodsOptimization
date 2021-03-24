from typing import List
from typing import Callable
from SupportFuntions.matrix_operations import add_vector, scale_vector, chebyshev_norm


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
