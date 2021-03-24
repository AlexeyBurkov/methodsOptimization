import math
from typing import List

from MultiDimMinimization.minimization import FirstGradientMethodConstStep
from SupportFuntions.matrix_operations import euclid_norm


# def function(x):
#     return -(x ** 5 - 5 * x ** 3 + 10 * x ** 2 - 5 * x)
# a_0 = -3
# b_0 = -2

def function(x: List[float]) -> float:
    return x[0] * x[0] + 2 * x[1] * x[1] + 3 * x[0] + 2 * x[1] + math.sin(x[0] + 2 * x[1])


def grad_function(x: List[float]) -> List[float]:
    return [2 * x[0] + 3 + math.cos(x[0] + 2 * x[1]), 4 * x[1] + 2 + 2 * math.cos(x[0] + 2 * x[1])]


if __name__ == '__main__':
    tol = 0.0001
    ws = FirstGradientMethodConstStep(grad_function, 4 / (10 + math.sqrt(17) + math.sqrt(41)),
                                      tol, [500., 1000.])
    while not ws.test_grad():
        ws.iterate()
    x, _, c = ws.get_result()
    print(x)
    print(c)
    print(euclid_norm(grad_function(x)))
