from typing import Callable


class UniformSearch:
    def __init__(self, func: Callable, left: float, right: float, tol: float, rang_m: int):
        if left > right:
            raise ValueError("Invalid Interval!")
        if tol < 0.:
            raise ValueError("Invalid tolerance!")
        if rang_m < 3:
            raise ValueError("Invalid rang of search!")
        self._f = func
        self._a = left
        self._b = right
        self._f_a = 0.
        self._f_b = 0.
        self._tol = tol
        self._res_a = left
        self._res_b = right
        self._f_count = 0
        self._m = rang_m

    def iterate(self):
        if self._f_count == 0:
            self._f_a = self._f(self._a)
            self._f_b = self._f(self._b)
            self._f_count += 2
        step = abs(self._res_b - self._res_a) / self._m
        f_grid = [0. for _ in range(self._m + 1)]
        f_grid[0] = self._f_a
        f_grid[self._m] = self._f_b
        for i in range(1, self._m):
            f_grid[i] = self._f(self._res_a + step * i)
        self._f_count += (self._m - 1)
        j = 0
        for i in range(1, self._m):
            if f_grid[j] >= f_grid[i]:
                j = i
        self._res_b = self._res_a + (step * (j + 1))
        self._res_a += (step * (j - 1))
        self._f_a = f_grid[j - 1]
        self._f_b = f_grid[j + 1]

    def test_result(self):
        return abs(self._res_b - self._res_a) < self._tol

    def get_result(self):
        return self._res_a, self._res_b, self._f_count

    def restart(self):
        self._res_a = self._a
        self._res_b = self._b
        self._f_count = 0

    def set_rang(self, new_rang: int):
        self._m = new_rang

    def set_tolerance(self, new_tol: float):
        self._tol = new_tol


class GoldenRatioSearch:
    def __init__(self, func: Callable, left: float, right: float, tol: float):
        if left > right:
            raise ValueError("Invalid Interval!")
        if tol < 0.:
            raise ValueError("Invalid tolerance!")
        self._f = func
        self._a = left
        self._b = right
        self._tol = tol
        self._res_a = left
        self._res_b = right
        self._f_count = 0
        self._f_p1 = 0.
        self._p1 = 0.
        self._f_p2 = 0.
        self._p2 = 0.
        self._alpha = (3 - 5 ** (1 / 2)) / 2
        self._need_update_first = True
        self._need_update_second = True

    def iterate(self):
        if self._need_update_first:
            self._p2 = self._res_a + self._res_b - self._p2
            self._f_p1 = self._f(self._p1)
            self._f_count += 1
            self._need_update_first = False
        if self._need_update_second:
            self._p2 = self._res_a + self._alpha * (self._res_b - self._res_a)
            self._f_p2 = self._f(self._p2)
            self._f_count += 1
            self._need_update_second = False
        if self._f_p1 <= self._f_p2:
            self._res_b = self._p2
            self._p2 = self._p1
            self._f_p2 = self._f_p1
            self._need_update_first = True
        else:
            self._res_a = self._p1
            self._p1 = self._p2
            self._f_p1 = self._f_p2
            self._need_update_second = True

    def test_result(self):
        return abs(self._res_b - self._res_a) < self._tol

    def get_result(self):
        return self._res_a, self._res_b, self._f_count

    def restart(self):
        self._res_a = self._a
        self._res_b = self._b
        self._need_update_first = True
        self._need_update_second = True
        self._f_count = 0

    def set_tolerance(self, new_tol: float):
        self._tol = new_tol
