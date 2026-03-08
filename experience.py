


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

second_array = []
for i in range(7):
    x = random.uniform((v/2)/C, (2*v)/C)  # свой x для каждой точки
    second_array.append(round(L*2/C + x, 12))

all_arrays.append(second_array)
lengths2 = [round(t * C / 2, 2) for t in second_array]


current_array = second_array
for array_num in range(3, 7):
    next_array = []
    x_values = []  
    
    for val in current_array:
        x = random.uniform((v/2)/C, (2*v)/C)  # свой x для каждой точки
        x_values.append(x)
        next_array.append(round(val + x, 12))
    
    all_arrays.append(next_array)
    lengths = [round(t * C / 2, 2) for t in next_array]
    
    current_array = next_array
if array_num == 3:
    third_array = all_arrays[2]
elif array_num == 4:
    fourth_array = all_arrays[3]
elif array_num == 5:
    fifth_array = all_arrays[4]
elif array_num == 6:
    sixth_array = all_arrays[5]



first_array = all_arrays[0] 
second_array = all_arrays[1] 
third_array = all_arrays[2] 
fourth_array = all_arrays[3] 
fifth_array = all_arrays[4] 
sixth_array = all_arrays[5] 







