import numpy as np
from scipy import integrate
# Параметры
y0 = 0.1
k = 0.1
x0 = 1
x1 = 30
step = 1


# Функция для вычисления L(x)
def compute_L(x):
    """Вычисляет L(x) = интеграл от 1 до x sqrt(1 + 1/(t*ln(0.5))^2) dt"""
    ln_half = np.log(0.5)

    def integrand(t):
        if t == 0:
            return np.sqrt(1 + 0)
        return np.sqrt(1 + 1 / (t * ln_half) ** 2)

    L, error = integrate.quad(integrand, x0, x)
    return L


# Создаем таблицу значений
x_values = np.arange(x0, x1 + step, step)
L_values = []
y_values = []

print("=" * 80)
print("ТАБЛИЦА ЗНАЧЕНИЙ ФУНКЦИИ y(x) = y₀ + k·L(x)")
print("=" * 80)
print(f"Параметры: y₀ = {y0}, k = {k}")
print(f"L(x) = ∫₁ˣ √(1 + 1/(t·ln(0.5))²) dt")
print("=" * 80)
print(f"{'x':^4} | {'L(x)':^12} | {'k·L(x)':^12} | {'y(x)':^12} | {'Δy':^10} | {'y(x) округл.':^12}")
print("-" * 80)

for i, x in enumerate(x_values):
    L = compute_L(x)
    kL = k * L
    y = y0 + kL

    L_values.append(L)
    y_values.append(y)

    # Вычисляем прирост от предыдущего значения
    if i == 0:
        delta_y = 0
    else:
        delta_y = y_values[i] - y_values[i - 1]

    print(f"{x:^4} | {L:^12.8f} | {kL:^12.8f} | {y:^12.8f} | {delta_y:^10.8f} | {round(y, 4):^12}")

print("=" * 80)

# Дополнительные вычисления
print("\n" + "=" * 80)
print("СТАТИСТИЧЕСКИЙ АНАЛИЗ y(x)")
print("=" * 80)

# Основные статистики
y_min = min(y_values)
y_max = max(y_values)
y_range = y_max - y_min
x_min = x_values[y_values.index(y_min)]
x_max = x_values[y_values.index(y_max)]

print(f"Начальное значение: y({x0}) = {y_values[0]:.8f}")
print(f"Конечное значение:  y({x1}) = {y_values[-1]:.8f}")
print(f"Минимальное значение: y({x_min}) = {y_min:.8f}")
print(f"Максимальное значение: y({x_max}) = {y_max:.8f}")
print(f"Общий прирост: Δy = {y_values[-1] - y_values[0]:.8f}")
print(f"Размах значений: {y_range:.8f}")
print()

# Средний прирост
avg_growth = (y_values[-1] - y_values[0]) / (len(y_values) - 1)
print(f"Средний прирост на шаг: {avg_growth:.8f}")

# Анализ по интервалам
print("\nАнализ прироста по интервалам:")
print(f"{'Интервал':^12} {'Δy':^12} {'Средний Δy/шаг':^15}")
print("-" * 45)

intervals = [(1, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30)]
for start, end in intervals:
    idx_start = start - 1
    idx_end = end - 1
    delta = y_values[idx_end] - y_values[idx_start]
    avg_delta = delta / (end - start)
    print(f"[{start:2d}, {end:2d}]   {delta:^12.8f}   {avg_delta:^15.8f}")

print("=" * 80)

# Проверка на линейность
print("\n" + "=" * 80)
print("ПРОВЕРКА НА ЛИНЕЙНОСТЬ")
print("=" * 80)
print("Если бы L(x) было линейной функцией (L(x) = a·x + b),")
print("то y(x) тоже была бы линейной: y(x) = y₀ + k·(a·x + b)")
print()

# Вычисляем коэффициенты линейной регрессии для L(x)
n = len(x_values)
sum_x = sum(x_values)
sum_y = sum(L_values)
sum_xy = sum(x * L for x, L in zip(x_values, L_values))
sum_x2 = sum(x ** 2 for x in x_values)

a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
b = (sum_y - a * sum_x) / n

print(f"Линейная аппроксимация L(x) ≈ {a:.6f}·x + {b:.6f}")
print(f"Фактически: L(30) = {L_values[-1]:.6f}")
print(f"По линейной аппроксимации: {a * 30 + b:.6f}")
print(f"Отклонение: {abs(L_values[-1] - (a * 30 + b)):.6f}")

# Для y(x)
a_y = k * a
b_y = y0 + k * b
print(f"\nСоответствующая y(x) ≈ {a_y:.6f}·x + {b_y:.6f}")
print(f"Фактически: y(30) = {y_values[-1]:.6f}")
print(f"По линейной аппроксимации: {a_y * 30 + b_y:.6f}")
print(f"Отклонение: {abs(y_values[-1] - (a_y * 30 + b_y)):.6f}")
print("=" * 80)

import matplotlib.pyplot as plt


# Параметры
y0 = 0.1
k = 0.1
x0 = 1
x1 = 30
step = 1


# Функция для вычисления L(x) с округлением до 0.001
def compute_L_rounded(x):
    """Вычисляет L(x) с округлением результата"""
    ln_half = np.log(0.5)

    def integrand(t):
        return np.sqrt(1 + 1 / (t * ln_half) ** 2)

    L, error = integrate.quad(integrand, x0, x)
    return np.round(L, 10)  # Вычисляем с запасом точности


# Создаем таблицу значений с округлением до 0.001
x_values = np.arange(x0, x1 + step, step)
y_values_rounded = []

print("=" * 70)
print("ТАБЛИЦА ЗНАЧЕНИЙ y(x) С ТОЧНОСТЬЮ ДО 0.001")
print("=" * 70)
print(f"{'x':^4} | {'L(x)':^12} | {'y(x) точное':^12} | {'y(x) округл.':^12} | {'Разность':^10}")
print("-" * 70)

for x in x_values:
    L = compute_L_rounded(x)
    y_exact = y0 + k * L
    y_rounded = np.round(y_exact, 3)  # Округляем до 0.001
    y_values_rounded.append(y_rounded)

    difference = y_rounded - y_exact

    print(f"{x:^4} | {L:^12.6f} | {y_exact:^12.8f} | {y_rounded:^12.3f} | {difference:^10.6f}")

print("=" * 70)

# Построение графика с точностью 0.001
fig = plt.figure(figsize=(14, 10))

# 1. Основной график с округленными значениями
ax1 = plt.subplot(2, 2, 1)
bars = ax1.bar(x_values, y_values_rounded,
               color=plt.cm.viridis(np.linspace(0, 1, len(x_values))),
               edgecolor='black', linewidth=0.8, alpha=0.8)

ax1.set_xlabel('x', fontsize=12, fontweight='bold')
ax1.set_ylabel('y(x) (округлено до 0.001)', fontsize=12, fontweight='bold')
ax1.set_title('Столбчатая диаграмма y(x) с точностью 0.001',
              fontsize=14, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_xticks(x_values)

# Добавляем значения на столбцы
for i, (x, y) in enumerate(zip(x_values, y_values_rounded)):
    ax1.text(x, y + 0.002, f'{y:.3f}',
             ha='center', va='bottom', fontsize=7, fontweight='bold')

# 2. График с точками и соединением
ax2 = plt.subplot(2, 2, 2)
# Рисуем линию
ax2.plot(x_values, y_values_rounded, 'k-', linewidth=1, alpha=0.5, zorder=1)

# Рисуем точки с цветом в зависимости от значения
scatter = ax2.scatter(x_values, y_values_rounded,
                      c=y_values_rounded, cmap='coolwarm', s=120,
                      edgecolors='black', linewidth=1.5, zorder=2)

ax2.set_xlabel('x', fontsize=12, fontweight='bold')
ax2.set_ylabel('y(x) (округлено до 0.001)', fontsize=12, fontweight='bold')
ax2.set_title('Точечный график y(x) с цветовой кодировкой',
              fontsize=14, fontweight='bold', pad=15)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(x_values)

# Добавляем цветовую шкалу
cbar = plt.colorbar(scatter, ax=ax2, pad=0.01)
cbar.set_label('Значение y(x)', fontsize=10, fontweight='bold')

# 3. График ошибки округления
ax3 = plt.subplot(2, 2, 3)

# Вычисляем точные значения для сравнения
y_exact_values = []
for x in x_values:
    L = compute_L_rounded(x)
    y_exact_values.append(y0 + k * L)

# Ошибка округления
rounding_error = [rounded - exact for rounded, exact in zip(y_values_rounded, y_exact_values)]

bars_error = ax3.bar(x_values, rounding_error,
                     color=['red' if err > 0 else 'blue' for err in rounding_error],
                     edgecolor='black', linewidth=0.5, alpha=0.7)

ax3.set_xlabel('x', fontsize=12, fontweight='bold')
ax3.set_ylabel('Ошибка округления', fontsize=12, fontweight='bold')
ax3.set_title('Ошибка при округлении до 0.001',
              fontsize=14, fontweight='bold', pad=15)
ax3.grid(True, alpha=0.3, axis='y')
ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax3.set_xticks(x_values)

# Добавляем значения ошибок
for i, (x, err) in enumerate(zip(x_values, rounding_error)):
    if abs(err) > 0.0001:  # Показываем только значимые ошибки
        va = 'bottom' if err > 0 else 'top'
        ax3.text(x, err, f'{err:.6f}',
                 ha='center', va=va, fontsize=6)

# 4. График приращений с округлением
ax4 = plt.subplot(2, 2, 4)
delta_y = np.diff(y_values_rounded)
delta_y = np.insert(delta_y, 0, 0)  # Добавляем 0 для x=1

# Рисуем ступенчатую функцию
ax4.step(x_values, y_values_rounded, where='mid',
         color='green', linewidth=2.5, alpha=0.7, label='y(x)')

# Дополнительные точки
ax4.scatter(x_values, y_values_rounded, color='darkgreen',
            s=50, zorder=3, edgecolors='black', linewidth=1)

ax4.set_xlabel('x', fontsize=12, fontweight='bold')
ax4.set_ylabel('y(x) (округлено до 0.001)', fontsize=12, fontweight='bold')
ax4.set_title('Ступенчатый график y(x)',
              fontsize=14, fontweight='bold', pad=15)
ax4.grid(True, alpha=0.3)
ax4.set_xticks(x_values)
ax4.legend()

# Добавляем значения на ступеньках
for i, (x, y) in enumerate(zip(x_values, y_values_rounded)):
    ax4.text(x, y + 0.003, f'{y:.3f}',
             ha='center', va='bottom', fontsize=7,
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))

plt.suptitle(f'График функции y(x) = {y0} + {k}·L(x) с точностью до 0.001',
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# Дополнительный подробный график
fig2, ax5 = plt.subplots(figsize=(15, 8))

# Создаем сетку для точного позиционирования
x_pos = np.arange(len(x_values))
width = 0.6

# Рисуем основной график с точками
line, = ax5.plot(x_values, y_values_rounded, 'o-',
                 color='darkblue', linewidth=2, markersize=8,
                 markerfacecolor='lightblue', markeredgecolor='darkblue',
                 markeredgewidth=1.5, label='y(x) с точностью 0.001')

ax5.set_xlabel('x', fontsize=14, fontweight='bold')
ax5.set_ylabel('y(x)', fontsize=14, fontweight='bold')
ax5.set_title('Детальный график y(x) с точностью до 0.001',
              fontsize=16, fontweight='bold', pad=20)
ax5.grid(True, alpha=0.3, linestyle='--')
ax5.set_xticks(x_values)

# Устанавливаем точные деления на оси y с шагом 0.05 для лучшей читаемости
from matplotlib.ticker import MultipleLocator

ax5.yaxis.set_major_locator(MultipleLocator(0.05))
ax5.yaxis.set_minor_locator(MultipleLocator(0.01))

# Добавляем горизонтальные линии сетки для точного чтения значений
ax5.grid(True, which='major', alpha=0.4, linestyle='-')
ax5.grid(True, which='minor', alpha=0.2, linestyle=':')

# Добавляем точные значения с точностью 0.001
for i, (x, y) in enumerate(zip(x_values, y_values_rounded)):
    # Размещаем подписи сверху или снизу в зависимости от положения
    offset = 0.003 if i % 2 == 0 else -0.01
    va = 'bottom' if offset > 0 else 'top'

    ax5.annotate(f'{y:.3f}', xy=(x, y), xytext=(0, offset * 100),
                 textcoords='offset points', ha='center', va=va,
                 fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3",
                           facecolor="yellow",
                           alpha=0.8,
                           edgecolor='black'))

# Добавляем область под кривой
ax5.fill_between(x_values, 0, y_values_rounded, alpha=0.1, color='blue')

# Легенда с информацией
info_text = f'y(x) = {y0} + {k}·L(x)\nТочность: 0.001'
ax5.text(0.02, 0.98, info_text, transform=ax5.transAxes,
         fontsize=12, verticalalignment='top',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))

# Вычисляем и показываем статистику на графике
y_min = min(y_values_rounded)
y_max = max(y_values_rounded)
y_range = y_max - y_min
y_avg = np.mean(y_values_rounded)

stats_text = f'Статистика:\nMin: {y_min:.3f} (x={x_values[np.argmin(y_values_rounded)]})\nMax: {y_max:.3f} (x={x_values[np.argmax(y_values_rounded)]})\nРазмах: {y_range:.3f}\nСреднее: {y_avg:.3f}'
ax5.text(0.98, 0.02, stats_text, transform=ax5.transAxes,
         fontsize=10, verticalalignment='bottom', horizontalalignment='right',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8))

plt.tight_layout()
plt.show()

# Вывод итоговой статистики
print("\n" + "=" * 70)
print("ИТОГОВАЯ СТАТИСТИКА (с точностью 0.001)")
print("=" * 70)

print(f"\nДиапазон значений y(x):")
print(f"  Начальное: y(1) = {y_values_rounded[0]:.3f}")
print(f"  Конечное:  y(30) = {y_values_rounded[-1]:.3f}")
print(f"  Минимум:   y({x_values[np.argmin(y_values_rounded)]}) = {y_min:.3f}")
print(f"  Максимум:  y({x_values[np.argmax(y_values_rounded)]}) = {y_max:.3f}")
print(f"  Размах:    {y_range:.3f}")

print(f"\nПриращения:")
print(f"  Максимальное Δy: {max(np.diff(y_values_rounded)):.3f}")
print(f"  Минимальное Δy:  {min(np.diff(y_values_rounded[1:])):.3f}")  # Исключаем первый 0
print(f"  Среднее Δy:      {np.mean(np.diff(y_values_rounded[1:])):.3f}")

# Анализ уникальных значений
unique_values = np.unique(y_values_rounded)
print(f"\nУникальные значения (с точностью 0.001):")
print(f"  Всего уникальных значений: {len(unique_values)}")
print(f"  Из {len(y_values_rounded)} точек")

# Проверка монотонности
is_monotonic = all(y_values_rounded[i] <= y_values_rounded[i + 1] for i in range(len(y_values_rounded) - 1))
print(f"\nПроверка свойств:")
print(f"  Функция монотонно возрастает: {'ДА' if is_monotonic else 'НЕТ'}")

# Значения, которые наиболее близки к "красивым" числам
nice_numbers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
print(f"\nБлизость к круглым числам:")
for nice in nice_numbers:
    closest_idx = np.argmin(np.abs(np.array(y_values_rounded) - nice))
    closest_value = y_values_rounded[closest_idx]
    difference = abs(closest_value - nice)
    if difference < 0.01:  # Ближе чем на 0.01
        print(f"  y({x_values[closest_idx]}) = {closest_value:.3f} "
              f"(отклонение от {nice}: {difference:.3f})")

print("=" * 70)

