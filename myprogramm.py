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
experimentaldata=processing(experience.all_arrays[0])
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
radiuses_value=radius_long(experience.all_arrays[0])
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

# numbers1 = input_seven_numbers(1)
# numbers2 = input_seven_numbers(2)
# numbers3 = input_seven_numbers(3)

 
numbers1 = experience.all_arrays[1]
numbers2 = experience.all_arrays[2]
numbers3 = experience.all_arrays[3]
numbers4 = experience.all_arrays[4]
numbers5 = experience.all_arrays[5]




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
    return [-t * c / 2 + all_long for t in t1]

initial_points = list(zip(border_x, border_y))

t1_arrays = [
    numbers1,  # массив 1
    numbers2,  # массив 2  
    numbers3,  # массив 3
    numbers4,  # массив 4
    numbers5   # массив 5
]

all_points = [initial_points]  # начальное положение
all_long0 = experience.L
# all_long0=50

# Для отладки - посмотрим, какие сдвиги получаются
print(f"Начальная all_long: {all_long0}")
print("-" * 50)

# Делаем ровно 5 сдвигов (по одному на каждый массив)
for i in range(5):
    shifts = delta(t1_arrays[i], all_long0)
    print(f"Сдвиг {i+1}:")
    print(f"  Массив t1: {[round(t, 10) for t in t1_arrays[i]]}")
    print(f"  Сдвиги (м): {[round(s, 6) for s in shifts]}")
    print(f"  all_long до сдвига: {all_long0}")
    
    new_set = new_points(all_points[-1], shifts)
    all_points.append(new_set)
    
    
    print(f"  all_long после сдвига: {all_long0}")
    print(f"  Средний сдвиг: {np.mean(shifts)}")
    print("-" * 50)

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
ax.set_xlim(-50, 100)
ax.set_ylim(-50, 100)
ax.grid(True, alpha=0.3)
line, = ax.plot([], [], 'bo-', linewidth=2, markersize=8)
title = ax.set_title('')


frames_per_transition = 30
total_frames = 5 * frames_per_transition + 1

def animate(frame):
    transition = frame // frames_per_transition
    alpha = (frame % frames_per_transition) / frames_per_transition
    
    if transition >= 5:
        points = all_points[5]
        title.set_text('Финальное положение')
    else:
        p1 = all_points[transition]
        p2 = all_points[transition + 1]
        points = [(p1[i][0] * (1 - alpha) + p2[i][0] * alpha,
                   p1[i][1] * (1 - alpha) + p2[i][1] * alpha) for i in range(7)]
        title.set_text(f'Сдвиг {transition + 1} из 5')
    
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    line.set_data(x, y)
    return line, title

ani = animation.FuncAnimation(fig, animate, frames=total_frames, interval=50, blit=True, repeat=False)
plt.show()



