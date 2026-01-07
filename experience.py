import math

import numpy as np
from scipy import integrate

y0 = 0.1
k = 0.1
x0 = 1
x1 = 30
step = 5


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
step = 5


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
#сигналы снимаются каждый месяц то есть удлиненние численно равно скорости (всё в м)
#координата крепления лининй (35, 35)
def all_time(speeds):
    t1=[]
    c=300000
    all_long=50
    for speed in speeds:
        t1.append(2*(all_long+speed/100)/c) #[t]=m*s/km
    return t1
def half_time(speeds):
    t2=[]
    c=300000
    coord_o=35
    for speed in speeds:
        t2.append(2*((coord_o-speed)**2+(coord_o-(math.log(speed, 0.5)+30))**2)**0.5/c)
    return t2
t1_values=all_time(y_values)
t2_values=half_time(x_values)
print(all_time(y_values))
print(half_time(x_values))
print(x_values)
print(y_values)

#график времени


fig, (ax1) = plt.subplots(1, 1, figsize=(15, 5))

#t1 и t2 от x_values
ax1.plot(x_values, t1_values, 'bo-', linewidth=2, markersize=6, label='t1 (прямой сигнал)')
ax1.plot(x_values, t2_values, 'rs-', linewidth=2, markersize=6, label='t2 (отраженный сигнал)')
ax1.set_xlabel('x, м', fontsize=12)
ax1.set_ylabel('Время, с*м/км', fontsize=12)
ax1.set_title('Время сигналов от координаты x', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.ticklabel_format(axis='y', style='sci', scilimits=(-6,-6))

plt.tight_layout()
plt.show()

