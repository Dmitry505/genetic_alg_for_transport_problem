from ortools.linear_solver import pywraplp
from reader import read_transportation_data
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




