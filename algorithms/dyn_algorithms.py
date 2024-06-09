from ortools.linear_solver import pywraplp
from project.reader import read_transportation_data
import time

def solve_transportation_problem(filename):
    # Читаем данные из файла
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data(filename)
    
    # Создаем решатель
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None, None

    # Определяем переменные
    x = {}  # Переменные для количества транспортируемых товаров
    y = {}  # Бинарные переменные для учета фиксированных затрат
    for i in range(num_factories):
        for j in range(num_stores):
            x[(i, j)] = solver.IntVar(0, solver.infinity(), f'x[{i},{j}]')
            y[(i, j)] = solver.BoolVar(f'y[{i},{j}]')

    # Задаем ограничения
    # Ограничения по производству
    for i in range(num_factories):
        solver.Add(solver.Sum([x[i, j] for j in range(num_stores)]) <= production[i])

    # Ограничения по спросу
    for j in range(num_stores):
        solver.Add(solver.Sum([x[i, j] for i in range(num_factories)]) >= demand[j])

    # Связь переменных x и y
    for i in range(num_factories):
        for j in range(num_stores):
            solver.Add(x[(i, j)] <= y[(i, j)] * demand[j])

    # Определяем целевую функцию
    objective = solver.Objective()
    for i in range(num_factories):
        for j in range(num_stores):
            objective.SetCoefficient(x[(i, j)], costs[i][j])
            objective.SetCoefficient(y[(i, j)], fixed_costs[i][j])
    objective.SetMinimization()

    # Измерение времени решения задачи
    start_time = time.time()
    
    # Решаем задачу
    status = solver.Solve()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Обработка результата
    if status == pywraplp.Solver.OPTIMAL:
        total_cost = 0
        for i in range(num_factories):
            for j in range(num_stores):
                if y[i, j].solution_value() > 0:
                    total_cost += x[i, j].solution_value() * costs[i][j] + fixed_costs[i][j]
        return total_cost, elapsed_time
    else:
        return None, elapsed_time

def process_files(file_list):
    results = []
    for filename in file_list:
        total_cost, elapsed_time = solve_transportation_problem(filename)
        results.append((filename, total_cost, elapsed_time))
    
    with open("data/din_prog_alg_results.txt", "w") as f:
        for filename, total_cost, elapsed_time in results:
            f.write(f"File: {filename}, Total Cost: {total_cost}, Elapsed Time: {elapsed_time:.4f} seconds\n")

# Список файлов для обработки
file_list = ["data/data_1.txt", "data/data_2.txt", "data/data_3.txt", "data/data_4.txt", "data/data_5.txt", "data/data_6.txt", "data/data_7.txt", "data/data_8.txt", "data/data_9.txt", "data/data_10.txt", "data/data_11.txt", "data/data_12.txt", "data/data_13.txt", "data/data_14.txt", "data/data_15.txt", "data/data_16.txt", "data/data_17.txt", "data/data_18.txt", "data/data_19.txt", "data/data_20.txt"]

# Обработка файлов
process_files(file_list)
