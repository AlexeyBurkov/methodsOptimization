from typing import List


def next_unique_combination(comb: List[int], max_value: int):
    x = comb.copy()
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
