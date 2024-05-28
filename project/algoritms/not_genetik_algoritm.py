import numpy as np
import time


def solve_transportation_problem(costs, supplies, demands, fixed_costs):
    """
    Решение транспортной задачи с фиксированными доплатами.

    Аргументы:
    costs (numpy.ndarray): Матрица затрат на транспортировку.
    supplies (list): Список доступных запасов у поставщиков.
    demands (list): Список потребностей потребителей.
    fixed_costs (numpy.ndarray): Матрица фиксированных доплат.

    Возвращает:
    list: Список поставок в формате (поставщик, потребитель, объем поставки, затраты).
    float: Общие затраты на транспортировку.
    float: Время работы алгоритма.
    """
    start_time = time.time()

    num_suppliers = len(supplies)
    num_consumers = len(demands)

    # Инициализация плана поставок
    allocation = np.zeros((num_suppliers, num_consumers), dtype=int)

    # Потребности и запасы
    supply = supplies.copy()
    demand = demands.copy()

    # Пока есть не удовлетворенные потребности или неиспользованные запасы
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        min_cost = float('inf')
        min_i = -1
        min_j = -1

        # Поиск минимальной стоимости с учетом фиксированных доплат
        for i in range(num_suppliers):
            for j in range(num_consumers):
                if supply[i] > 0 and demand[j] > 0:
                    effective_cost = costs[i][j] + fixed_costs[i][j]
                    if effective_cost < min_cost:
                        min_cost = effective_cost
                        min_i = i
                        min_j = j

        # Определение объема поставки
        allocation_amount = min(supply[min_i], demand[min_j])
        allocation[min_i][min_j] = allocation_amount
        supply[min_i] -= allocation_amount
        demand[min_j] -= allocation_amount

    # Подсчет общих затрат
    total_cost = 0
    for i in range(num_suppliers):
        for j in range(num_consumers):
            if allocation[i][j] > 0:
                total_cost += allocation[i][j] * costs[i][j] + fixed_costs[i][j]

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Формирование списка результатов
    result = []
    for i in range(num_suppliers):
        for j in range(num_consumers):
            if allocation[i][j] > 0:
                result.append((i, j, allocation[i][j], allocation[i][j] * costs[i][j] + fixed_costs[i][j]))

    return result, total_cost, elapsed_time


# Пример данных
costs = np.array([
    [8, 6, 10],
    [9, 12, 13],
    [14, 9, 16]
])

supplies = [100, 150, 200]
demands = [130, 160, 160]

fixed_costs = np.array([
    [3, 2, 5],
    [6, 4, 3],
    [2, 3, 1]
])

result, total_cost, elapsed_time = solve_transportation_problem(costs, supplies, demands, fixed_costs)

# Вывод результатов
print("Результаты поставок (Поставщик, Потребитель, Объем поставки, Затраты):")
for res in result:
    print(f"Поставщик {res[0] + 1} -> Потребитель {res[1] + 1}: Объем поставки = {res[2]}, Затраты = {res[3]}")

print(f"Общие затраты: {total_cost}")
print(f"Время выполнения: {elapsed_time:.4f} секунд")
