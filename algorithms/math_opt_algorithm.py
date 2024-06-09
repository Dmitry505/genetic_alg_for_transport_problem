import pulp
import time
from project.reader import read_transportation_data

def solve_transportation_problem(filename="transportation_data.txt"):
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data(filename)

    # Создаем LP задачу
    prob = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

    # Создаем переменные для количества товаров, отправляемых с фабрики i в магазин j
    x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for j in range(num_stores)] for i in range(num_factories)]
    
    # Создаем бинарные переменные для фиксированных затрат
    y = [[pulp.LpVariable(f"y_{i}_{j}", cat='Binary') for j in range(num_stores)] for i in range(num_factories)]

    # Функция цели: минимизировать затраты на транспортировку и фиксированные затраты
    prob += pulp.lpSum(costs[i][j] * x[i][j] + fixed_costs[i][j] * y[i][j] for i in range(num_factories) for j in range(num_stores)), "Total_Cost"

    # Ограничения на производство
    for i in range(num_factories):
        prob += pulp.lpSum(x[i][j] for j in range(num_stores)) <= production[i], f"Production_Constraint_{i}"

    # Ограничения на спрос
    for j in range(num_stores):
        prob += pulp.lpSum(x[i][j] for i in range(num_factories)) == demand[j], f"Demand_Constraint_{j}"

    # Ограничения на фиксированные затраты (если отправляем товар, то должны платить фиксированные затраты)
    for i in range(num_factories):
        for j in range(num_stores):
            prob += x[i][j] <= production[i] * y[i][j], f"Fixed_Cost_Constraint_{i}_{j}"

    # Измеряем время начала решения задачи
    start_time = time.time()

    # Решаем задачу
    prob.solve()

    # Измеряем время окончания решения задачи
    end_time = time.time()

    # Печатаем результаты
    status = pulp.LpStatus[prob.status]
    total_cost = pulp.value(prob.objective)
    execution_time = end_time - start_time

    return status, total_cost, execution_time

def run_multiple_files(filenames, output_filename="results.txt"):
    with open(output_filename, "w") as outfile:
        outfile.write("Filename,Status,Total Cost,Execution Time\n")
        for filename in filenames:
            status, total_cost, execution_time = solve_transportation_problem(filename)
            outfile.write(f"{filename},{status},{total_cost},{execution_time}\n")

# Список файлов для обработки
file_list = ["data/data_1.txt", "data/data_2.txt", "data/data_3.txt", "data/data_4.txt", "data/data_5.txt", "data/data_6.txt", "data/data_7.txt", "data/data_8.txt", "data/data_9.txt", "data/data_10.txt", "data/data_11.txt", "data/data_12.txt", "data/data_13.txt", "data/data_14.txt", "data/data_15.txt", "data/data_16.txt", "data/data_17.txt", "data/data_18.txt", "data/data_19.txt", "data/data_20.txt"]

# Запуск функции для обработки всех файлов
run_multiple_files(file_list, "C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/math_alg_results.txt")
