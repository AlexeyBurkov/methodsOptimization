from typing import List
from typing import Callable
from SupportFuntions.matrix_operations import add_vector, scale_vector, chebyshev_norm, inner_product
from SystemSolution.solution import linear_system_solution_llt
from OneDimMinimization.minimization import GoldenRatioSearch


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


class SecondGradientMethodOneDimMinStep:
    def __init__(self, func: Callable, dfunc: Callable, gesse_func: Callable, tol: float, x0: List[float]):
        self._g_f = gesse_func
        self._df = dfunc
        self._f = func
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

        def g(a: float):
            return self._f(add_vector(self._x, scale_vector(a, direction)))

        step_max = 0.
        f_step_max = g(step_max)
        self._f_count += 1
        while True:
            next_f = g(step_max + 1.)
            self._f_count += 1
            step_max += 1.0
            if f_step_max < next_f:
                break
            f_step_max = next_f
        step_min = 0.
        if (step_max - 2.) > 0.:
            step_min = step_max - 1.
        gs = GoldenRatioSearch(g, step_min, step_max, self._tol)
        while not gs.test_result():
            gs.iterate()
        res_1, res_2, f_count = gs.get_result()
        step = (res_1 + res_2) / 2

        self._f_count += f_count
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
