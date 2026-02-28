import math

import matplotlib
matplotlib.use('TkAgg')
from fontTools.merge.util import current_time
from matplotlib.pyplot import scatter

import experience
c=300000

numbers1 = experience.all_arrays[1]
numbers2 = experience.all_arrays[2]
numbers3 = experience.all_arrays[3]
numbers4 = experience.all_arrays[4]
numbers5 = experience.all_arrays[5]

longs1 = [experience.L] * 7  
longs2 = [experience.all_arrays[1][i] * c / 2 for i in range(7)]
longs3 = [experience.all_arrays[2][i] * c / 2 for i in range(7)]
longs4 = [experience.all_arrays[3][i] * c / 2 for i in range(7)]
longs5 = [experience.all_arrays[4][i] * c / 2 for i in range(7)]

t1_arrays = [
    numbers1,  # массив 1
    numbers2,  # массив 2  
    numbers3,  # массив 3
    numbers4,  # массив 4
    numbers5   # массив 5
]
all_longs = [
    longs1,
    longs2,
    longs3,
    longs4,
    longs5,
]
#проверка опасности скорости движения точек границы
def processing(t1, longs):
    exp_value=[]
    for t, long in zip(t1, longs):
        exp_value.append(t*c / 2 - long)
    return exp_value


all_dangers = []  
all_colors = []  

crit = 1
st1 = 1
st2 = 2

for array_idx in range(1, 6):  
    experimentaldata = processing(experience.all_arrays[array_idx], all_longs[array_idx-1])
    
    danger = []
    for value in experimentaldata:
        if value < crit:
            danger.append(0)
        elif value < crit + st1:
            danger.append(1)
        elif value < crit + st2:
            danger.append(2)
        else:
            danger.append(3)
    
    all_dangers.append(danger)

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
    all_colors.append(colors)
    
    print(f"Опасность для массива {array_idx+1}: {danger}")
    print(f"Цвета для массива {array_idx+1}: {colors}")
    print("-" * 30)

#поиск графического описания границы
#пусть 7 шнуров протянуты под углами 0, pi/12, pi/6, pi/4, pi/3, pi*5/12, pi/2
#нужно использовтать значения времени t2, чтобы получить длину радиус-вектора
coord_o = float(input("Введите координаты x=y точки крепления шнуров: "))
degrees=[0, math.pi/12, math.pi/6, math.pi/4, math.pi/3, math.pi*5/12, math.pi/2]
def radius_long(t2):
    radius=[]
    c=300000
    for t in t2:
        radius.append(t*c / 2)
    return radius
radiuses_value=radius_long(experience.all_arrays[0])
print(radiuses_value)
def border_coordinates(radiuses):
    x_coord=[]
    y_coord=[]
    c=300000
    for r, d in zip(radiuses, degrees):
        x_coord.append(coord_o-r*math.cos(d))
        y_coord.append(coord_o-r*math.sin(d))

    return x_coord, y_coord
border_x, border_y = border_coordinates(radiuses_value)
print (border_x)
print (border_y)

 




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


def delta(t1, longs):
    c = 300000
    return [-t * c / 2 + long for t, long in zip(t1, longs)]

initial_points = list(zip(border_x, border_y))



all_points = [initial_points]  # начальное положение

for i in range(5):
    shifts = delta(t1_arrays[i], all_longs[i])

    
    new_set = new_points(all_points[-1], shifts)
    all_points.append(new_set)
    
    
   

print(f"Создано наборов точек: {len(all_points)}")

# Визуализируем все наборы точек для проверки
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, points in enumerate(all_points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    axes[idx].plot(x, y, 'bo-', linewidth=2, markersize=8)
    axes[idx].set_title(f'Набор {idx} (после {idx} сдвигов)')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].set_xlim(-50, 300)
    axes[idx].set_ylim(-50, 300)
    axes[idx].set_aspect('equal')

plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.grid(True, alpha=0.3)

scat = ax.scatter([], [], c=[], s=100, edgecolors='black', linewidth=1.5, zorder=5)
line, = ax.plot([], [], 'k-', linewidth=1.5, alpha=0.5, zorder=1)  
title = ax.set_title('')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='green', edgecolor='black', label='Уровень 0 (безопасно)'),
    Patch(facecolor='yellow', edgecolor='black', label='Уровень 1 (слабая опасность)'),
    Patch(facecolor='orange', edgecolor='black', label='Уровень 2 (средняя опасность)'),
    Patch(facecolor='red', edgecolor='black', label='Уровень 3 (высокая опасность)')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=8)


frames_per_transition = 30
total_frames = 5 * frames_per_transition + 1

def animate(frame):
    transition = frame // frames_per_transition
    alpha = (frame % frames_per_transition) / frames_per_transition
    
    if transition >= 5:
        points = all_points[5]
        title.set_text('Финальное положение')
        current_colors = all_colors[4]  
    else:
        p1 = all_points[transition]
        p2 = all_points[transition + 1]
        points = [(p1[i][0] * (1 - alpha) + p2[i][0] * alpha,
                   p1[i][1] * (1 - alpha) + p2[i][1] * alpha) for i in range(7)]
        title.set_text(f'Сдвиг {transition + 1} из 5')
        current_colors = all_colors[transition]
    
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    
    scat.set_offsets(np.c_[x, y])
    scat.set_color(current_colors)  
    line.set_data(x, y)
    
    return scat, line, title
ani = animation.FuncAnimation(fig, animate, frames=total_frames, interval=50, blit=True, repeat=False)
plt.show()



