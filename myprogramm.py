import math

import matplotlib
matplotlib.use('TkAgg')
from fontTools.merge.util import current_time
from matplotlib.pyplot import scatter

import experience
#проверка опасности скорости движения точек границы
def processing(t1):
    exp_value=[]
    c=300000
    all_long=50
    for t in t1:
        #exp_value.append((t*c/2-all_long)*100)
        exp_value.append((t*c / 2 - all_long) * 100)
    return exp_value
experimentaldata=processing(experience.t1_values)
danger = []
crit = 1
st1 = 1
st2 = 2
for i in range (len(experimentaldata)):
    if experimentaldata[i] < crit:
        danger.append(0)
    if experimentaldata[i] > crit and experimentaldata[i] < crit + st1:
        danger.append(1)
    if experimentaldata[i] > crit+st1 and experimentaldata[i] < crit + st2:
        danger.append(2)
    if experimentaldata[i] > crit + st2:
        danger.append(3)
print (danger)
#на графике будем отмечать шнуры разными цветами взависимости от опасности
colors = []
for d in danger:
    if d == 0:
        colors.append('green')
    elif d == 1:
        colors.append('yellow')
    elif d == 2:
        colors.append('orange')
    elif d == 3:
        colors.append('red')

#поиск графического описания границы
#пусть 7 шнуров протянуты под углами 0, pi/12, pi/6, pi/4, pi/3, pi*5/12, pi/2
#нужно использовтать значения времени t2, чтобы получить длину радиус-вектора
degrees=[0, math.pi/12, math.pi/6, math.pi/4, math.pi/3, math.pi*5/12, math.pi/2]
def radius_long(t2):
    radius=[]
    c=300000
    for t in t2:
        #radius.append(t*c/2)
        radius.append(t*c / 2)
    return radius
radiuses_value=radius_long(experience.t2_values)
print(radiuses_value)
def border_coordinates(radiuses):
    x_coord=[]
    y_coord=[]
    c=300000
    coord_o=35
    for r, d in zip(radiuses, degrees):
        x_coord.append(coord_o-r*math.cos(d))
        y_coord.append(coord_o-r*math.sin(d))

    return x_coord, y_coord
border_x, border_y = border_coordinates(radiuses_value)
print (border_x)
print (border_y)

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time
plt.close('all')

# plt.figure(figsize=(8, 6))
# for i in range(len(border_x)):
#     plt.scatter(border_x[i], border_y[i], c=colors[i], s=150,
#                 edgecolors='black', linewidth=1.5, zorder=5,
#                 label=f'Опасность {danger[i]}' if i == 0 else "")
# plt.plot(border_x, border_y, 'b-', alpha=0.7)
# plt.scatter([35], [35], c='blue', s=200, marker='*')
# plt.xlabel('X координата')
# plt.ylabel('Y координата')
# plt.title('Координаты границы')
# plt.grid(True)
# plt.axis('equal')
# plt.tight_layout()


#сдвигаем точки для получения новой границы, будем сдвигать вдоль касательной на значние удлинения провода, затем создаём новый график
from typing import List, Tuple
def new_points(points: List[Tuple[float, float]],
                            shifts: List[float]) -> List[Tuple[float, float]]:
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    s = np.array(shifts)

    n = len(points)
    derivatives = np.zeros(n)

    for i in range(1, n - 1):
        dx = x[i + 1] - x[i - 1]
        dy = y[i + 1] - y[i - 1]
        if dx != 0:
            derivatives[i] = dy / dx

    if x[1] - x[0] != 0:
        derivatives[0] = (y[1] - y[0]) / (x[1] - x[0])

    if x[-1] - x[-2] != 0:
        derivatives[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])

    tangent_lengths = np.sqrt(1 + derivatives ** 2)
    unit_dx = 1/tangent_lengths
    unit_dy = derivatives / tangent_lengths

    new_x = x - s * unit_dx
    new_y = y - s * unit_dy

    return list(zip(new_x, new_y))
#чтобы получить значения сдвига нужно использовать значения t1
def delta(t1, all_long):
    shifts=[]
    c=300000
    for t in t1:
        #shifts.append(t*c-2*all_long)
        shifts.append(-(t*c  - 2 * all_long))
    return shifts
all_long=50
shifts=delta(experience.t1_values, all_long)
print(radiuses_value)
points = list(zip(border_x, border_y))
shifted = new_points(points, shifts)



#второй график
new_border_x, new_border_y = zip(*shifted)
# plt.figure(figsize=(8, 6))
# for i in range(len(new_border_x)):
#     plt.scatter(new_border_x[i], new_border_y[i], c=colors[i], s=150,
#                 edgecolors='black', linewidth=1.5, zorder=5,
#                 label=f'Опасность {danger[i]}' if i == 0 else "")
# plt.plot(new_border_x, new_border_y, 'b-', alpha=0.7)
# plt.scatter([35], [35], c='blue', s=200, marker='*')
# plt.xlabel('X координата')
# plt.ylabel('Y координата')
# plt.title('Координаты новой границы')
# plt.grid(True)
# plt.axis('equal')
# plt.tight_layout()



# следующий набор сдвигов (второй)
# shifts2=delta(experience.t1_values2)
# print(radiuses_value)
# points2 = list(zip(new_border_x, new_border_y))
# shifted2 = new_points(points2, shifts2)

# # график вторых сдвигов (третий)
# new_border_x2, new_border_y2 = zip(*shifted2)
# plt.figure(figsize=(8, 6))
# for i in range(len(new_border_x2)):
#     plt.scatter(new_border_x2[i], new_border_y2[i], c=colors[i], s=150,
#                 edgecolors='black', linewidth=1.5, zorder=5,
#                 label=f'Опасность {danger[i]}' if i == 0 else "")
# plt.plot(new_border_x2, new_border_y2, 'b-', alpha=0.7)
# plt.scatter([35], [35], c='blue', s=200, marker='*')
# plt.xlabel('X координата')
# plt.ylabel('Y координата')
# plt.title('Координаты новой границы2')
# plt.grid(True)
# plt.axis('equal')
# plt.tight_layout()



#Делаем анимированный график со сдвигами

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 40)
ax.set_ylim(0, 40)
ax.grid(True, alpha=0.7)
ax.set_title('Движение границы')

scatter = ax.scatter(border_x, border_y, c='blue', s=100)
line, = ax.plot(border_x, border_y, 'b-', alpha=0.7)

update_count = 0
all_updates = 10
last_update_time = time.time()


# def update(frame):
#     global border_x, border_y, last_update_time, update_count
#     current_time = time.time()
#     if current_time - last_update_time >= 2 and update_count < all_updates:
#         border_x = new_border_x
#         border_y = new_border_y
#         scatter.set_offsets(np.c_[border_x, border_y])
#         last_update_time = current_time
#         update_count += 1
#     return scatter,
# anim = FuncAnimation(fig, update, frames=None, interval=100, blit=True)
def update(frame):
    global border_x, border_y, update_count
    if update_count < all_updates:
        t = frame / 10.0
        
        current_x = [border_x[i] + t * (new_border_x[i] - border_x[i]) 
                    for i in range(len(border_x))]
        current_y = [border_y[i] + t * (new_border_y[i] - border_y[i]) 
                    for i in range(len(border_y))]
        
        scatter.set_offsets(np.c_[current_x, current_y])
        line.set_data(current_x, current_y)
        
        if frame >= 10:
            update_count += 1
    return scatter, line

anim = FuncAnimation(fig, update, frames=range(11), interval=200, blit=True, repeat=True)

plt.tight_layout()
plt.show()

#получим сразу 10 положений точек для соответственно 10и снятых экспериментально наборов t1 (которые характеризуют сдвиги)
# def new_points(points: List[Tuple[float, float]],
#               shifts: List[float]) -> List[Tuple[float, float]]:
#     x = np.array([p[0] for p in points])
#     y = np.array([p[1] for p in points])
#     s = np.array(shifts)
#
#     n = len(points)
#     derivatives = np.zeros(n)
#
#     for i in range(1, n - 1):
#         dx = x[i + 1] - x[i - 1]
#         dy = y[i + 1] - y[i - 1]
#         if dx != 0:
#             derivatives[i] = dy / dx
#
#     if x[1] - x[0] != 0:
#         derivatives[0] = (y[1] - y[0]) / (x[1] - x[0])
#
#     if x[-1] - x[-2] != 0:
#         derivatives[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])
#
#     tangent_lengths = np.sqrt(1 + derivatives ** 2)
#     unit_dx = 1/tangent_lengths
#     unit_dy = derivatives / tangent_lengths
#
#     new_x = x - s * unit_dx
#     new_y = y - s * unit_dy
#
#     return list(zip(new_x, new_y))
#
# def delta(t1, all_long):
#     c = 300000
#     return [-(t*c - 2 * all_long) for t in t1]
# initial_points = list(zip(border_x, border_y))
# all_points_sets = [initial_points]
# all_points_sets_with_all_long = []
#
# first_all_long = 50
# all_points_sets_with_all_long.append(first_all_long)
#
# for iteration in range(3):
#
#     t1_values = []
#     for i in range(7):
#         value = float(input(f"t1_{i+1}: "))
#         t1_values.append(value)
#
#     shifts = delta(t1_values, first_all_long)
#     prev_points = all_points_sets[-1]
#     new_set = new_points(prev_points, shifts)
#     all_points_sets.append(new_set)
#     avg_shift = np.mean(shifts)
#     first_all_long += avg_shift
#     all_points_sets_with_all_long.append(first_all_long)


import tkinter as tk
from tkinter import simpledialog, messagebox


def input_seven_numbers(iteration):
    root = tk.Tk()
    root.withdraw()

    while True:
        dialog = tk.Toplevel()
        dialog.title(f"Ввод экспериментальных точек {iteration}")
        dialog.geometry("400x200")

        entry = tk.Entry(dialog, width=40, font=('Arial', 11))
        entry.pack(pady=10)
        entry.focus_set()

        result = []

        def submit():
            nonlocal result
            try:
                text = entry.get().replace(' ', '')
                numbers = text.split(',')

                if len(numbers) != 7:
                    messagebox.showerror("Ошибка", "Введите 7 значений")
                    return

                result = [float(x) for x in numbers]
                dialog.destroy()

            except ValueError:
                messagebox.showerror("Ошибка", "Введены некорректные значния")

        def cancel():
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="OK", command=submit,
                  bg='#4CAF50', fg='white', width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=cancel,
                  bg='#f44336', fg='white', width=10).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()

        if result:
            return result

numbers1 = input_seven_numbers(1)
numbers2 = input_seven_numbers(2)
numbers3 = input_seven_numbers(3)


# from typing import List, Tuple
# import numpy as np
#
#
# def new_points(points: List[Tuple[float, float]],
#                shifts: List[float]) -> List[Tuple[float, float]]:
#     x = np.array([p[0] for p in points])
#     y = np.array([p[1] for p in points])
#     s = np.array(shifts)
#
#     n = len(points)
#     derivatives = np.zeros(n)
#
#     for i in range(1, n - 1):
#         dx = x[i + 1] - x[i - 1]
#         dy = y[i + 1] - y[i - 1]
#         if dx != 0:
#             derivatives[i] = dy / dx
#
#     if x[1] - x[0] != 0:
#         derivatives[0] = (y[1] - y[0]) / (x[1] - x[0])
#
#     if x[-1] - x[-2] != 0:
#         derivatives[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])
#
#     tangent_lengths = np.sqrt(1 + derivatives ** 2)
#     unit_dx = 1 / tangent_lengths
#     unit_dy = derivatives / tangent_lengths
#
#     new_x = x - s * unit_dx
#     new_y = y - s * unit_dy
#
#     return list(zip(new_x, new_y))
#
#
# def delta(t1, all_long):
#     c = 300000
#     return [-(t * c - 2 * all_long) for t in t1]
#
# initial_points = list(zip(border_x, border_y))
#
# t1_arrays = [
#     numbers1,  # первый набор
#     numbers2,  # второй набор
#     numbers3  # третий набор
# ]
#
# all_points_sets = [initial_points]
# all_points_sets_with_all_long = []
#
# first_all_long = 50
# all_points_sets_with_all_long.append(first_all_long)
#
# for iteration in range(3):
#     t1_values = t1_arrays[iteration]
#
#     shifts = delta(t1_values, first_all_long)
#     prev_points = all_points_sets[-1]
#     new_set = new_points(prev_points, shifts)
#     all_points_sets.append(new_set)
#     avg_shift = np.mean(shifts)
#     first_all_long += avg_shift
#     all_points_sets_with_all_long.append(first_all_long)


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List, Tuple


def new_points(points: List[Tuple[float, float]], shifts: List[float]) -> List[Tuple[float, float]]:
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    s = np.array(shifts)

    derivatives = np.zeros(len(points))
    for i in range(1, len(points) - 1):
        dx = x[i + 1] - x[i - 1]
        if dx != 0:
            derivatives[i] = (y[i + 1] - y[i - 1]) / dx
    if x[1] - x[0] != 0:
        derivatives[0] = (y[1] - y[0]) / (x[1] - x[0])
    if x[-1] - x[-2] != 0:
        derivatives[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])

    tangent_lengths = np.sqrt(1 + derivatives ** 2)
    new_x = x - s / tangent_lengths
    new_y = y - s * derivatives / tangent_lengths
    return list(zip(new_x, new_y))


def delta(t1, all_long):
    c = 300000
    return [-(t * c - 2 * all_long) for t in t1]



initial_points = list(zip(border_x, border_y))

t1_arrays = [
    numbers1,  # первый набор
    numbers2,  # второй набор
    numbers3  # третий набор
]

all_points = [initial_points]
all_long = 50

for i in range(3):
    shifts = delta(t1_arrays[i], all_long)
    new_set = new_points(all_points[-1], shifts)
    all_points.append(new_set)
    all_long += np.mean(shifts)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(5, 45)
ax.set_ylim(5, 25)
ax.grid(True, alpha=0.3)
line, = ax.plot([], [], 'bo-', linewidth=2, markersize=8)
title = ax.set_title('')


def animate(frame):
    t = frame / 50
    idx = int(t)
    alpha = t - idx

    if idx >= 2:
        points = all_points[3]
    else:
        p1 = all_points[idx]
        p2 = all_points[idx + 1]
        points = [(p1[i][0] * (1 - alpha) + p2[i][0] * alpha,
                   p1[i][1] * (1 - alpha) + p2[i][1] * alpha) for i in range(7)]

    x = [p[0] for p in points]
    y = [p[1] for p in points]
    line.set_data(x, y)
    title.set_text(f'Набор {idx + 1} → {idx + 2}' if idx < 2 else 'Набор 3')
    return line, title


ani = animation.FuncAnimation(fig, animate, frames=150, interval=50, blit=True)
plt.show()

# 0.000334, 0.000344, 0.000354, 0.000364, 0.000354, 0.000344, 0.000334
# 0.0003342, 0.0003442, 0.0003542, 0.0003642, 0.0003542, 0.0003442, 0.0003342
# 0.0003344, 0.0003444, 0.0003544, 0.0003644, 0.0003544, 0.0003444, 0.0003344