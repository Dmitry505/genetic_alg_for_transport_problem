import pulp
import time
from project.reader import read_transportation_data

def read_transportation_data(filename="transportation_data.txt"):
    with open(filename, "r") as f:
        num_factories, num_stores = map(int, f.readline().split())
        f.readline()  # Пропускаем пустую строку

        production = list(map(int, f.readline().split()))
        demand = list(map(int, f.readline().split()))
        f.readline()  # Пропускаем пустую строку

        costs = []
        for _ in range(num_factories):
            costs.append(list(map(int, f.readline().split())))
        f.readline()  # Пропускаем пустую строку

        fixed_costs = []
        for _ in range(num_factories):
            fixed_costs.append(list(map(int, f.readline().split())))

    return num_factories, num_stores, production, demand, costs, fixed_costs

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
    print("Status:", pulp.LpStatus[prob.status])
    print("Total Cost:", pulp.value(prob.objective))
    print("Execution Time:", end_time - start_time, "seconds")

    return prob

# Запуск функции для решения транспортной задачи
solve_transportation_problem("C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/data_20.txt")
