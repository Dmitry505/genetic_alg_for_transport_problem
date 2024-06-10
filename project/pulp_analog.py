import pulp
import time
from reader import read_transportation_data


def solve_transportation_problem_pulp(filename="transportation_data.txt"):
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data(filename)

    # Создаем LP задачу
    prob = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

    # Создаем переменные для количества товаров, отправляемых с фабрики i в магазин j
    x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for j in range(num_stores)] for i in
         range(num_factories)]

    # Создаем бинарные переменные для фиксированных затрат
    y = [[pulp.LpVariable(f"y_{i}_{j}", cat='Binary') for j in range(num_stores)] for i in range(num_factories)]

    # Функция цели: минимизировать затраты на транспортировку и фиксированные затраты
    prob += pulp.lpSum(costs[i][j] * x[i][j] + fixed_costs[i][j] * y[i][j] for i in range(num_factories) for j in
                       range(num_stores)), "Total_Cost"

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
