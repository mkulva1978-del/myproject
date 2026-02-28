# import math

# import numpy as np
# from scipy import integrate

# y0 = 10
# k = 0.1
# x0 = 1
# x1 = 30
# step = 5


# def compute_L(x):
#     ln_half = np.log(0.5)

#     def integrand(t):
#         if t == 0:
#             return np.sqrt(1 + 0)
#         return np.sqrt(1 + 1 / (t * ln_half) ** 2)

#     L, error = integrate.quad(integrand, x0, x)
#     return L



# x_values = np.arange(x0, x1 + step, step)
# L_values = []
# y_values = []


# for i, x in enumerate(x_values):
#     L = compute_L(x)
#     kL = k * L
#     y = y0 + kL

#     L_values.append(L)
#     y_values.append(y)

#     if i == 0:
#         delta_y = 0
#     else:
#         delta_y = y_values[i] - y_values[i - 1]




# # Вычисляем коэффициенты линейной регрессии для L(x)
# n = len(x_values)
# sum_x = sum(x_values)
# sum_y = sum(L_values)
# sum_xy = sum(x * L for x, L in zip(x_values, L_values))
# sum_x2 = sum(x ** 2 for x in x_values)

# a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
# b = (sum_y - a * sum_x) / n


# # Для y(x)
# a_y = k * a
# b_y = y0 + k * b

# import matplotlib.pyplot as plt


# # Параметры
# y0 = 10
# k = 0.1
# x0 = 1
# x1 = 30
# step = 5


# def compute_L_rounded(x):

#     ln_half = np.log(0.5)

#     def integrand(t):
#         return np.sqrt(1 + 1 / (t * ln_half) ** 2)

#     L, error = integrate.quad(integrand, x0, x)
#     return np.round(L, 10)  # Вычисляем с запасом точности



# x_values = np.arange(x0, x1 + step, step)
# y_values_rounded = []


# #расчёт значений времени для прямого сигнала t1 и отраженного t2
# #сигналы снимаются каждый месяц то есть удлиненние численно равно скорости (всё в м)
# #координата крепления лининй (35, 35)
# def all_time(speeds):
#     t1=[]
#     c=300000
#     all_long=50
#     for speed in speeds:
#         t1.append(2 * (all_long + speed / 100) / c)
#         #t1.append(2*(all_long+speed/100)) #[t]=m*s/km
#     return t1
# def half_time(speeds):
#     t2=[]
#     c=300000
#     coord_o=35
#     for speed in speeds:
#         t2.append(2 * ((coord_o - speed) ** 2 + (coord_o - (math.log(speed, 0.5) + 30)) ** 2) ** 0.5 / c)
#         #t2.append(2*((coord_o-speed)**2+(coord_o-(math.log(speed, 0.5)+30))**2)**0.5)
#     return t2
# t1_values=all_time(y_values)
# t2_values=half_time(x_values)
# # print(all_time(y_values))
# # print(half_time(x_values))
# # print(x_values)
# # print(y_values)


# #создание следующего набора точек для смещения границы (результаты за следующий месяц)

# def all_time2(speeds):
#     t1=[]
#     c=300000
#     all_long=50
#     for speed in speeds:
#         t1.append(2*(all_long+speed/100)/c) #[t]=m*s/km
#         #t1.append(2 * (all_long + 2*speed / 100))
#     return t1
# def half_time2(speeds):
#     t2=[]
#     c=300000
#     coord_o=35
#     for speed in speeds:
#        t2.append(2 * ((coord_o - speed) ** 2 + (coord_o - (math.log(speed, 0.5) + 30)) ** 2) ** 0.5 / c)
#         #t2.append(2*((coord_o-speed)**2+(coord_o-(math.log(speed, 0.5)+30))**2)**0.5)
#     return t2
# t1_values2=all_time(y_values)
# #import myprogramm
# #x_values2=myprogramm.new_border_x
# #t2_values2=half_time(x_values2)
# #print(all_time2(y_values))
# #print(half_time2(x_values2))


import random
import math

# Константа скорости света (для пересчета, так как везде делим на 300000)
C = 300000

# Входные данные
L = float(input("Введите начальную длину провода L: "))
v = float(input("Введите начальную скорость первой точки v: "))

# Список для хранения всех 6 массивов
all_arrays = []

# --- Шаг 2: Создание первого массива (7 точек, монотонно) ---
first_array = []
# Опорное значение: 2*(L/2)/300000 = L/300000
base_value = L / C
# Диапазон отклонения: от -10 до +10 метров в пересчете на время
min_val = 2*(L-10)/C  # (L - 20)/C
max_val = 2*(L+10)/C  # (L + 20)/C

# Генерируем строго монотонно возрастающую последовательность
for i in range(7):
    if i == 0:
        # Первая точка может быть любой в диапазоне
        new_val = random.uniform(min_val, max_val)
    else:
        # Каждая следующая точка должна быть БОЛЬШЕ предыдущей
        prev_val = first_array[i-1]
        # Генерируем пока не получим число больше предыдущего
        while True:
            candidate = random.uniform(min_val, max_val)
            if candidate > prev_val:
                new_val = candidate
                break
    first_array.append(round(new_val, 12))  # Округляем для читаемости

all_arrays.append(first_array)
print(f"\nМассив 1 (из L): {first_array}")

# --- Шаг 3: Создание второго массива (из первого + x) ---
second_array = []
for t in first_array:
    # x случайно от (v/2)/300000 до (2*v)/300000  ← ИСПРАВЛЕНО!
    x = random.uniform((2*v)/C, (4*v)/C)
    second_array.append(round(t + x, 12))

all_arrays.append(second_array)
print(f"Массив 2 (1-й + x): {second_array}")

# --- Шаг 4: Создание массивов 3, 4, 5, 6 (последовательно) ---
# Текущий массив для преобразований (начинаем со второго)
current_array = second_array

for array_num in range(3, 7):  # номера 3, 4, 5, 6
    next_array = []
    for val in current_array:
        # x случайно от (v/2)/300000 до (2*v)/300000  ← ИСПРАВЛЕНО!
        x = random.uniform((2*v)/C, (4*v)/C)
        next_array.append(round(val + x, 12))
    
    all_arrays.append(next_array)
    print(f"Массив {array_num} (из {array_num-1} + x): {next_array}")
    current_array = next_array

# --- Шаг 5: Вывод результата ---
print("\n" + "="*40)
print("ИТОГОВЫЕ 6 МАССИВОВ:")
for idx, arr in enumerate(all_arrays, 1):
    print(f"Массив {idx}: {arr}")
