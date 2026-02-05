import math

import experience
#проверка опасности скорости движения точек границы
def processing(t1):
    exp_value=[]
    c=300000
    all_long=50
    for t in t1:
        exp_value.append((t*c/2-all_long)*100)
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
        radius.append(t*c/2)
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
import numpy as np


plt.figure(figsize=(8, 6))
for i in range(len(border_x)):
    plt.scatter(border_x[i], border_y[i], c=colors[i], s=150,
                edgecolors='black', linewidth=1.5, zorder=5,
                label=f'Опасность {danger[i]}' if i == 0 else "")
plt.plot(border_x, border_y, 'b-', alpha=0.7)
plt.scatter([35], [35], c='blue', s=200, marker='*')
plt.xlabel('X координата')
plt.ylabel('Y координата')
plt.title('Координаты границы')
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.show()

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
def delta(t1):
    shifts=[]
    all_long=50
    c=300000
    for t in t1:
        shifts.append(t*c-all_long)
    return shifts
shifts=delta(experience.t1_values)
print(radiuses_value)
points = list(zip(border_x, border_y))
shifted = new_points(points, shifts)

#второй график
new_border_x, new_border_y = zip(*shifted)
plt.figure(figsize=(8, 6))
for i in range(len(new_border_x)):
    plt.scatter(new_border_x[i], new_border_y[i], c=colors[i], s=150,
                edgecolors='black', linewidth=1.5, zorder=5,
                label=f'Опасность {danger[i]}' if i == 0 else "")
plt.plot(new_border_x, new_border_y, 'b-', alpha=0.7)
plt.scatter([35], [35], c='blue', s=200, marker='*')
plt.xlabel('X координата')
plt.ylabel('Y координата')
plt.title('Координаты новой границы')
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.show()