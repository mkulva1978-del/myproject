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

C = 300000

L = float(input("Введите начальную длину провода L: "))
v = float(input("Введите начальную скорость первой точки v: "))


all_arrays = []
first_array = []
base_value = L / C
min_val = 2*(L-10)/C  
max_val = 2*(L+10)/C  

for i in range(7):
    if i == 0:
        new_val = random.uniform(min_val, max_val)
    else:
        prev_val = first_array[i-1]
        while True:
            candidate = random.uniform(min_val, max_val)
            if candidate > prev_val:
                new_val = candidate
                break
    first_array.append(round(new_val, 12))  

all_arrays.append(first_array)
print(f"\nМассив 1 (из L): {first_array}")

second_array = []
for i in range(7):
    x = random.uniform((v/2)/C, (2*v)/C)  # свой x для каждой точки
    second_array.append(round(L*2/C + x, 12))

all_arrays.append(second_array)
print(f"\nМассив 2 (база {L*2/C:.12f} + x_i): {second_array}")
lengths2 = [round(t * C / 2, 2) for t in second_array]
print(f"  Длины 2 (м): {lengths2}")

# --- Массивы 3, 4, 5, 6 (из предыдущего + свой x для каждой точки) ---
current_array = second_array
for array_num in range(3, 7):
    next_array = []
    x_values = []  # для отладки
    
    for val in current_array:
        x = random.uniform((v/2)/C, (2*v)/C)  # свой x для каждой точки
        x_values.append(x)
        next_array.append(round(val + x, 12))
    
    all_arrays.append(next_array)
    print(f"\nМассив {array_num} (+ x_i): {next_array}")
    print(f"  Добавки x_i: {[round(x, 12) for x in x_values]}")
    lengths = [round(t * C / 2, 2) for t in next_array]
    print(f"  Длины (м): {lengths}")
    current_array = next_array
if array_num == 3:
    third_array = all_arrays[2]
elif array_num == 4:
    fourth_array = all_arrays[3]
elif array_num == 5:
    fifth_array = all_arrays[4]
elif array_num == 6:
    sixth_array = all_arrays[5]
print("\n" + "="*40)
print("ИТОГОВЫЕ 6 МАССИВОВ:")
for idx, arr in enumerate(all_arrays, 1):
    print(f"Массив {idx}: {arr}")

first_array = all_arrays[0] 
second_array = all_arrays[1] 
third_array = all_arrays[2] 
fourth_array = all_arrays[3] 
fifth_array = all_arrays[4] 
sixth_array = all_arrays[5] 







