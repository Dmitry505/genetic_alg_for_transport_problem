import numpy as np
import time


def solve_transportation_problem(supply, demand, variable_costs, fixed_costs):
    """
    Решает транспортную задачу с фиксированными платежами с использованием жадного алгоритма.

    :param list supply: Список объемов предложений от каждого поставщика.
    :param list demand: Список объемов спроса каждого потребителя.
    :param list variable_costs: Двумерный список переменных затрат на перевозку от каждого поставщика к каждому потребителю.
    :param list fixed_costs: Двумерный список фиксированных затрат на открытие маршрута от каждого поставщика к каждому потребителю.

    Возвращает:
    solution: Список кортежей (поставщик, потребитель, объем перевозки, затраты) для каждого маршрута.
    total_cost: Общие затраты на транспортировку.
    elapsed_time: Время выполнения алгоритма.
    """
    start_time = time.time()

    num_suppliers = len(supply)
    num_consumers = len(demand)

    supply = np.array(supply)
    demand = np.array(demand)
    variable_costs = np.array(variable_costs)
    fixed_costs = np.array(fixed_costs)

    solution = []

    used_routes = np.zeros((num_suppliers, num_consumers), dtype=bool)

    total_cost = 0

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        min_cost = float('inf')
        chosen_supplier = -1
        chosen_consumer = -1

        for i in range(num_suppliers):
            for j in range(num_consumers):
                if not used_routes[i][j]:
                    cost = variable_costs[i][j] + fixed_costs[i][j]
                else:
                    cost = variable_costs[i][j]

                if supply[i] > 0 and demand[j] > 0 and cost < min_cost:
                    min_cost = cost
                    chosen_supplier = i
                    chosen_consumer = j

        shipment = min(supply[chosen_supplier], demand[chosen_consumer])

        supply[chosen_supplier] -= shipment
        demand[chosen_consumer] -= shipment

        if not used_routes[chosen_supplier][chosen_consumer]:
            total_cost += fixed_costs[chosen_supplier][chosen_consumer]
            used_routes[chosen_supplier][chosen_consumer] = True
        total_cost += variable_costs[chosen_supplier][chosen_consumer] * shipment

        solution.append((chosen_supplier, chosen_consumer, shipment,
                         variable_costs[chosen_supplier][chosen_consumer] * shipment +
                         fixed_costs[chosen_supplier][chosen_consumer] if not used_routes[chosen_supplier][
                             chosen_consumer]
                         else variable_costs[chosen_supplier][chosen_consumer] * shipment))

    end_time = time.time()
    elapsed_time = end_time - start_time

    return solution, total_cost, elapsed_time


def output_data(supply, demand, variable_costs, fixed_costs):
    solution, total_cost, elapsed_time = solve_transportation_problem(supply, demand, variable_costs, fixed_costs)

    print(f"Общее время выполнения: {elapsed_time} секунд")
    print(f"Общие затраты: {total_cost}")
    print("Решение:")
    for supplier, consumer, shipment, cost in solution:
        print(f"Поставщик {supplier} -> Потребитель {consumer}: Объем перевозки {shipment}, Затраты {cost}")


if __name__ == '__main__':
    supply = [20, 30, 25]
    demand = [15, 25, 20, 15]
    variable_costs = [
        [8, 6, 10, 9],
        [9, 12, 13, 7],
        [14, 9, 16, 5]
    ]
    fixed_costs = [
        [100, 120, 150, 130],
        [110, 140, 160, 100],
        [130, 110, 180, 90]
    ]

    output_data(supply, demand, variable_costs, fixed_costs)
