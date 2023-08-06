import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def func(x, a, b):
    return 10 ** (a * x + b)


def func2(x, a, b):
    return a * (23.16 * x) ** b


class DataFit:
    def __init__(self, ls=23.16, b1=1.17 * 10 ** -5):
        self.ls = ls
        self.b1 = b1

    def fit_init(self, data):
        d2 = np.array([[float(i) for i in line.split('\t')] for line in data.split('\n') if len(line) > 0])
        return d2[:, 0], d2[:, 1]

    def fit_line(self, data):
        xd, yd = self.fit_init(data)

        (k, b), _ = curve_fit(func, np.array(xd), np.array(yd))
        y1 = 10 ** (xd * k + b)
        return (k, b), y1

    def fit_exp(self, data):
        xd, yd = self.fit_init(data)

        (k, b), _ = curve_fit(func2, np.array(xd), np.array(yd))
        y1 = k * ((self.ls * xd) ** b)
        return (k, b), y1
