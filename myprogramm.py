
# ИМПОРТЫ И НАСТРОЙКА МАТПЛОТЛИБ

import math
import matplotlib # для отображения окон
matplotlib.use('TkAgg')  # Указываем бэкенд для отображения графиков
from matplotlib.pyplot import scatter
import matplotlib.pyplot as plt # создание графиков
import matplotlib.animation as animation # FuncAnimation для анимации движения
import numpy as np # Массивы координат, производные, касательные
from typing import List, Tuple # Типизация аргументов функций
from matplotlib.patches import Rectangle, Patch #табличка с предупреждением, элементы легенды с цветами

import experience  # Импортируем подпрграмму с данными


c = 300000



# ПОЛУЧЕНИЕ ДАННЫХ ИЗ EXPERIENCE

# Массивы времен для 5 последовательных сдвигов точек(индексы 1-5)
numbers1 = experience.all_arrays[1]
numbers2 = experience.all_arrays[2]
numbers3 = experience.all_arrays[3]
numbers4 = experience.all_arrays[4]
numbers5 = experience.all_arrays[5]

# Пересчет времен в длины проводов для каждого сдвига
# longs1 - начальные длины (все равны experience.L)
# longs2-5 - длины после каждого сдвига
longs1 = [experience.L] * 7  
longs2 = [experience.all_arrays[1][i] * c / 2 for i in range(7)]
longs3 = [experience.all_arrays[2][i] * c / 2 for i in range(7)]
longs4 = [experience.all_arrays[3][i] * c / 2 for i in range(7)]
longs5 = [experience.all_arrays[4][i] * c / 2 for i in range(7)]

# Общие массивы:
t1_arrays = [numbers1, numbers2, numbers3, numbers4, numbers5]  # времена
all_longs = [longs1, longs2, longs3, longs4, longs5]            # длины



# ФУНКЦИЯ ДЛЯ РАСЧЕТА ОПАСНОСТИ

def processing(t1, longs):
    # Вычисляет отклонение текущей длины от начальной, т. е. скорость за промежуток времени между снятиями данных. Возвращает список отклонений в метрах

    exp_value = []
    for t, long in zip(t1, longs):
        exp_value.append(t * c / 2 - long)
    return exp_value



# РАСЧЕТ УРОВНЕЙ ОПАСНОСТИ ДЛЯ ВСЕХ МАССИВОВ

all_dangers = []  # Список списков с уровнями опасности (0-3)
all_colors = []   # Список списков с цветами для графика

# Критические значения для определения уровня опасности
crit = 1   
st1 = 1    
st2 = 2    

# Расчет для каждого из 5 массивов (индексы 1-5)
for array_idx in range(1, 6):
    # Получаем отклонения для текущего массива
    experimentaldata = processing(experience.all_arrays[array_idx], all_longs[array_idx-1])
    
    # Определяем уровень опасности для каждой точки
    danger = []
    for value in experimentaldata:
        if value < crit:
            danger.append(0)                    # безопасно
        elif value < crit + st1:
            danger.append(1)                    # слабая опасность
        elif value < crit + st2:
            danger.append(2)                    # средняя опасность
        else:
            danger.append(3)                    # высокая опасность
    
    all_dangers.append(danger)

    # Преобразуем уровни опасности в цвета для графика
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



# ПОСТРОЕНИЕ ГРАНИЦЫ ПО ДАННЫМ ПЕРВОГО МАССИВА

# Получаем координаты точки крепления шнуров
coord_o = float(input("Введите координаты x=y точки крепления шнуров: "))

# Углы для 7 шнуров (от 0 до 90 градусов)
degrees = [0, math.pi/12, math.pi/6, math.pi/4, math.pi/3, math.pi*5/12, math.pi/2]

def radius_long(t2):
    # Пересчитывает времена в радиусы (длины шнуров)
    radius = []
    for t in t2:
        radius.append(t * c / 2)
    return radius

# Получаем радиусы из первого массива (начальная граница)
radiuses_value = radius_long(experience.all_arrays[0])

def border_coordinates(radiuses):
    
    # Вычисляет координаты точек границы. Каждая точка находится на своем луче (угол из degrees) на расстоянии radius от точки крепления
    
    x_coord = []
    y_coord = []
    for r, d in zip(radiuses, degrees):
        x_coord.append(coord_o - r * math.cos(d))
        y_coord.append(coord_o - r * math.sin(d))
    return x_coord, y_coord

# Вычисляем координаты начальной границы
border_x, border_y = border_coordinates(radiuses_value)



# ФУНКЦИИ ДЛЯ ПЕРЕМЕЩЕНИЯ ТОЧЕК

def new_points(points: List[Tuple[float, float]], shifts: List[float]) -> List[Tuple[float, float]]:
    
    # Смещает точки вдоль касательной к кривой
    # points - исходные точки
    # shifts - величины смещения для каждой точки
    # Возвращает новые координаты точек
    
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    s = np.array(shifts)

    # Вычисляем производные (наклон касательной) в каждой точке
    derivatives = np.zeros(len(points))
    for i in range(1, len(points) - 1):
        dx = x[i + 1] - x[i - 1]
        if dx != 0:
            derivatives[i] = (y[i + 1] - y[i - 1]) / dx
    if x[1] - x[0] != 0:
        derivatives[0] = (y[1] - y[0]) / (x[1] - x[0])
    if x[-1] - x[-2] != 0:
        derivatives[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])

    # Вычисляем направление касательной и смещаем точки
    tangent_lengths = np.sqrt(1 + derivatives ** 2)
    new_x = x - s / tangent_lengths
    new_y = y - s * derivatives / tangent_lengths
    return list(zip(new_x, new_y))

def delta(t1, longs):
    
    # Вычисляет величину смещения для каждой точки
    # t1 - времена из текущего массива
    # longs - длины проводов для текущего массива
    
    return [-t * c / 2 + long for t, long in zip(t1, longs)]



# ПОСТРОЕНИЕ ВСЕХ НАБОРОВ ТОЧЕК (5 СДВИГОВ)

# Начальный набор точек (граница)
initial_points = list(zip(border_x, border_y))
all_points = [initial_points]

# Последовательно применяем 5 сдвигов
for i in range(5):
    shifts = delta(t1_arrays[i], all_longs[i])
    new_set = new_points(all_points[-1], shifts)
    all_points.append(new_set)



# ВИЗУАЛИЗАЦИЯ ВСЕХ 6 НАБОРОВ НА ОТДЕЛЬНЫХ ГРАФИКАХ

# fig, axes = plt.subplots(2, 3, figsize=(15, 10))
# axes = axes.flatten()

# for idx, points in enumerate(all_points):
#     x = [p[0] for p in points]
#     y = [p[1] for p in points]
#     axes[idx].plot(x, y, 'bo-', linewidth=2, markersize=8)
#     axes[idx].set_title(f'Набор {idx} (после {idx} сдвигов)')
#     axes[idx].grid(True, alpha=0.3)
#     axes[idx].set_xlim(-50, 300)
#     axes[idx].set_ylim(-50, 300)
#     axes[idx].set_aspect('equal')

# plt.tight_layout()
# plt.show()



# ПОДГОТОВКА АНИМАЦИИ

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.grid(True, alpha=0.3)

# Элементы анимации: точки (цветные) и линия
scat = ax.scatter([], [], c=[], s=100, edgecolors='black', linewidth=1.5, zorder=5)
line, = ax.plot([], [], 'k-', linewidth=1.5, alpha=0.5, zorder=1)  
title = ax.set_title('')


# КРАСНАЯ ТАБЛИЧКА ПРЕДУПРЕЖДЕНИЯ

# Прямоугольник-фон
warning_rect = Rectangle((10, 10), 30, 10, 
                         facecolor='red', alpha=0.7, 
                         edgecolor='darkred', linewidth=2,
                         visible=False, zorder=10)
ax.add_patch(warning_rect)

# Текст предупреждения
warning_text = ax.text(25, 15, '⚠ ОПАСНОСТЬ! ⚠', 
                       ha='center', va='center',
                       color='white', fontsize=12, fontweight='bold',
                       visible=False, zorder=11)


# ЛЕГЕНДА ДЛЯ ЦВЕТОВ

legend_elements = [
    Patch(facecolor='green', edgecolor='black', label='Уровень 0 (безопасно)'),
    Patch(facecolor='yellow', edgecolor='black', label='Уровень 1 (слабая опасность)'),
    Patch(facecolor='orange', edgecolor='black', label='Уровень 2 (средняя опасность)'),
    Patch(facecolor='red', edgecolor='black', label='Уровень 3 (высокая опасность)')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=8)



# НАСТРОЙКА ПАРАМЕТРОВ АНИМАЦИИ

frames_per_transition = 30  # количество кадров на один переход
total_frames = 5 * frames_per_transition + 1  # общее число кадров


# ФУНКЦИЯ АНИМАЦИИ

def animate(frame):
    
    # Функция, вызываемая для каждого кадра анимации
    # frame - номер текущего кадра
    
    # Определяем текущий переход (0-4) и фазу внутри перехода (0-1)
    transition = frame // frames_per_transition
    alpha = (frame % frames_per_transition) / frames_per_transition
    
    # Выбираем точки для отображения
    if transition >= 5:
        # Финальный кадр - показываем последний набор
        points = all_points[5]
        title.set_text('Финальное положение')
        current_colors = all_colors[4]  # цвета последнего массива
    else:
        # Плавный переход между наборами transition и transition+1
        p1 = all_points[transition]
        p2 = all_points[transition + 1]
        points = [(p1[i][0] * (1 - alpha) + p2[i][0] * alpha,
                   p1[i][1] * (1 - alpha) + p2[i][1] * alpha) for i in range(7)]
        title.set_text(f'Сдвиг {transition + 1} из 5')
        current_colors = all_colors[transition]
    
    # Извлекаем координаты
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    
    
    # ПРОВЕРКА НА КРАСНЫЕ ТОЧКИ
    
    has_red = 'red' in current_colors  # есть ли красные точки?
    warning_rect.set_visible(has_red)   # показываем/скрываем табличку
    warning_text.set_visible(has_red)
    
    # Обновляем графические элементы
    scat.set_offsets(np.c_[x, y])
    scat.set_color(current_colors)  
    line.set_data(x, y)
    
    return scat, line, title, warning_rect, warning_text


# ЗАПУСК АНИМАЦИИ

ani = animation.FuncAnimation(fig, animate, frames=total_frames, 
                              interval=50, blit=True, repeat=False)
plt.show()


