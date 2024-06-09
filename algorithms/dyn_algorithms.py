from ortools.linear_solver import pywraplp
from project.reader import read_transportation_data
import time

def solve_transportation_problem(filename="transportation_data.txt"):
    # Читаем данные из файла
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data(filename)
    
    # Создаем решатель
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

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

    # Выводим результат
    if status == pywraplp.Solver.OPTIMAL:
        print('Решение найдено:')
        total_cost = 0
        for i in range(num_factories):
            for j in range(num_stores):
                if y[i, j].solution_value() > 0:
                    total_cost += x[i, j].solution_value() * costs[i][j] + fixed_costs[i][j]
                print(f'Перевезти {x[i, j].solution_value()} единиц с завода {i} в магазин {j} с фиксированными затратами {fixed_costs[i][j] * y[i, j].solution_value()}')
        print('Общие затраты =', total_cost)
    else:
        print('Задача не имеет оптимального решения.')

    print(f'Время решения: {elapsed_time:.4f} секунд')

solve_transportation_problem("C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/data_1.txt")
