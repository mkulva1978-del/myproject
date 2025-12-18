import numpy as np
from scipy import integrate

y0 = 0.1
k = 0.1
x0 = 1
x1 = 30
step = 1


def compute_L(x):
    ln_half = np.log(0.5)

    def integrand(t):
        if t == 0:
            return np.sqrt(1 + 0)
        return np.sqrt(1 + 1 / (t * ln_half) ** 2)

    L, error = integrate.quad(integrand, x0, x)
    return L



x_values = np.arange(x0, x1 + step, step)
L_values = []
y_values = []


for i, x in enumerate(x_values):
    L = compute_L(x)
    kL = k * L
    y = y0 + kL

    L_values.append(L)
    y_values.append(y)

    if i == 0:
        delta_y = 0
    else:
        delta_y = y_values[i] - y_values[i - 1]




# Вычисляем коэффициенты линейной регрессии для L(x)
n = len(x_values)
sum_x = sum(x_values)
sum_y = sum(L_values)
sum_xy = sum(x * L for x, L in zip(x_values, L_values))
sum_x2 = sum(x ** 2 for x in x_values)

a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
b = (sum_y - a * sum_x) / n


# Для y(x)
a_y = k * a
b_y = y0 + k * b

import matplotlib.pyplot as plt


# Параметры
y0 = 0.1
k = 0.1
x0 = 1
x1 = 30
step = 1


def compute_L_rounded(x):

    ln_half = np.log(0.5)

    def integrand(t):
        return np.sqrt(1 + 1 / (t * ln_half) ** 2)

    L, error = integrate.quad(integrand, x0, x)
    return np.round(L, 10)  # Вычисляем с запасом точности



x_values = np.arange(x0, x1 + step, step)
y_values_rounded = []


for x in x_values:
    L = compute_L_rounded(x)
    y_exact = y0 + k * L
    y_rounded = np.round(y_exact, 3)  # Округляем до 0.001
    y_values_rounded.append(y_rounded)

    difference = y_rounded - y_exact

#расчёт значений времени для прямого сигнала t1 и отраженного t2
def all_time(x):
    t1=[]
    c=300000
    for j in y_values:
        t1[j]=2*(50+y[j])/c






