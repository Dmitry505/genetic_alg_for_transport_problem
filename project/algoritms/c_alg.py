import subprocess
import shlex
import numpy as np


def run_transport_algorithm(supply, demand, cost, fixed_cost, max_generations,
                            population_size, mutation_rate, script="./algoritm_c") -> tuple:
    """ Функция для передачи данных в скрипт на C++ и получения результата от него

    :param list supply: Список поставок от каждого поставщика.
    :param list demand: Список спроса каждого потребителя.
    :param np.array cost: Матрица стоимости перевозок.
    :param np.array fixed_cost: Матрица фиксированных доплат.

    :return: Кортеж содержащий: Лучшее решение в формате (Поставщик, Потребитель, Объем, Стоимость), Общая оптимальная стоимость, Общее время выполнения всех запусков.
    :rtype: (tuple)
    """
    supply_str = ",".join(map(str, supply))
    demand_str = ",".join(map(str, demand))
    cost_str = ",".join(map(str, [item for sublist in cost for item in sublist]))
    fixed_cost_str = ",".join(map(str, [item for sublist in fixed_cost for item in sublist]))

    cmd = f'{script} {supply_str} {demand_str} {cost_str} {fixed_cost_str} {max_generations} {population_size} {mutation_rate}'
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    output = result.stdout.strip().split()

    best_fitness = float(output[0])
    execution_time = float(output[1])

    results = []
    for i in range(2, len(output), 4):
        supplier = int(output[i])
        consumer = int(output[i + 1])
        amount = int(output[i + 2])
        cost = float(output[i + 3])
        results.append((supplier, consumer, amount, cost))

    return results, best_fitness, execution_time


def find_best_solution(supply, demand, cost, fixed_cost, max_generations=1000,
                       population_size=50, mutation_rate=0.01, runs=10) -> tuple:
    """
    Выполняет генетический алгоритм несколько раз и возвращает лучшее решение.

    :param list supply: Список поставок от каждого поставщика.
    :param list demand: Список спроса каждого потребителя.
    :param np.array cost: Матрица стоимости перевозок.
    :param np.array fixed_cost: Матрица фиксированных доплат.
    :param int runs: Количество запусков алгоритма.

    :return: Кортеж содержащий: Лучшее решение в формате (Поставщик, Потребитель, Объем, Стоимость), Общая оптимальная стоимость, Общее время выполнения всех запусков.
    :rtype: (tuple)
    """
    best_results = None
    best_fitness = float('inf')
    total_execution_time = 0

    for _ in range(runs):
        results, fitness, execution_time = run_transport_algorithm(supply, demand, cost, fixed_cost, max_generations,
                                                                population_size, mutation_rate)
        total_execution_time += execution_time
        if fitness < best_fitness:
            best_fitness = fitness
            best_results = results

    return best_results, best_fitness, total_execution_time


if __name__ == '__main__':
    # Пример использования
    supply = [20, 30, 25]
    demand = [10, 15, 20, 30]
    cost = [[8, 6, 10, 9],
            [9, 12, 13, 7],
            [14, 9, 16, 5]]
    fixed_cost = [[1, 1, 2, 1],
                  [3, 2, 2, 3],
                  [4, 2, 3, 1]]

    best_results, best_fitness, total_execution_time = find_best_solution(supply, demand, cost, fixed_cost, runs=4)

    print("Оптимальный транспортный план:")
    print("Поставщик -> Потребитель | Размер поставки | стоимость")
    for result in best_results:
        supplier, consumer, amount, cost = result
        print(f"{supplier} -> {consumer} | {amount} | {cost:.2f}")

    print(f"\nОбщая оптимальная стоимость: {best_fitness:.2f}")
    print(f"Время выполнения : {total_execution_time:.2f} секунд")
