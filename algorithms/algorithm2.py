import numpy as np
import sys
import time
from scipy.optimize import linprog
from project.reader import read_transportation_data

def solve_transportation_problem(file_path, output_file):
    start_time = time.time()  # Запускаем таймер
    
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data(file_path)

    # Проверка правильности считанных данных
    print(f"num_factories: {num_factories}, num_stores: {num_stores}")
    print(f"production: {production}")
    print(f"demand: {demand}")
    print(f"costs: {costs}")
    print(f"fixed_costs: {fixed_costs}")

    # Дополнение массивов до нужных размеров
    if len(production) < num_factories:
        production.extend([0] * (num_factories - len(production)))
    if len(demand) < num_stores:
        demand.extend([0] * (num_stores - len(demand)))
    
    for i in range(len(costs)):
        if len(costs[i]) < num_stores:
            costs[i].extend([0] * (num_stores - len(costs[i])))
    for i in range(len(fixed_costs)):
        if len(fixed_costs[i]) < num_stores:
            fixed_costs[i].extend([0] * (num_stores - len(fixed_costs[i])))
    
    # Проверка балансировки задачи
    total_production = sum(production)
    total_demand = sum(demand)
    if total_production != total_demand:
        if total_production < total_demand:
            production.append(total_demand - total_production)
            costs.append([0] * num_stores)
            fixed_costs.append([0] * num_stores)
            num_factories += 1
        else:
            demand.append(total_production - total_demand)
            for row in costs:
                row.append(0)
            for row in fixed_costs:
                row.append(0)
            num_stores += 1

    # Преобразование данных для линейного программирования
    c = []
    A_eq = []
    b_eq = []
    bounds = []

    M = 1000000  # Большое число для метода больших чисел

    for i in range(num_factories):
        for j in range(num_stores):
            c.append(costs[i][j] + M * fixed_costs[i][j])
            bounds.append((0, None))

    for i in range(num_factories):
        A_eq.append([1 if i == k // num_stores else 0 for k in range(num_factories * num_stores)])
        b_eq.append(production[i])

    for j in range(num_stores):
        A_eq.append([1 if j == k % num_stores else 0 for k in range(num_factories * num_stores)])
        b_eq.append(demand[j])

    # Решение задачи линейного программирования
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    # Обработка и запись результатов
    with open(output_file, 'w') as f:
        if res.success:
            x = np.array(res.x).reshape((num_factories, num_stores))
            f.write(f"Статус решения: Успешно\n")
            for i in range(num_factories):
                for j in range(num_stores):
                    if x[i][j] > 0:
                        f.write(f"Транспортировка из фабрики {i} в магазин {j}: {x[i][j]:.2f} единиц с фиксированной доплатой {fixed_costs[i][j]}\n")
            total_cost = np.sum(x * np.array(costs)) + np.sum(np.array(fixed_costs) * (x > 0))
            f.write(f"Общая стоимость: {total_cost:.2f}\n")
        else:
            f.write("Решение не найдено\n")

    end_time = time.time()  # Завершаем таймер
    elapsed_time = end_time - start_time  # Вычисляем время выполнения

    # Записываем время выполнения в файл
    with open(output_file, 'a') as f:  # 'a' - режим дозаписи, чтобы сохранить предыдущие результаты
        f.write(f"Время выполнения: {elapsed_time:.4f} секунд\n")

# Пример использования
input_file = 'C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/data_20.txt'
output_file = 'C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/output.txt'
solve_transportation_problem(input_file, output_file)
