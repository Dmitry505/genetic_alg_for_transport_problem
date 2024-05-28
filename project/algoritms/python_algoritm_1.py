import numpy as np
import time
import random


# ToDo: Алгоритм
def genetic_algorithm_transportation(supply, demand, cost, fixed_cost, max_generations=1000,
                                     population_size=50, mutation_rate=0.01) -> tuple:
    """
    Решает транспортную задачу с использованием генетического алгоритма.

    :param list supply: Список поставок от каждого поставщика.
    :param list demand: Список спроса каждого потребителя.
    :param np.array cost: Матрица стоимости перевозок.
    :param np.array fixed_cost: Матрица фиксированных доплат.
    :param int max_generations: Максимальное число поколений
    :param int population_size: Размер популяции
    :param float mutation_rate: вероятность мутации

    :return: Кортеж содержащий: решение в формате (Поставщик, Потребитель, Объем, Стоимость), Общая оптимальная стоимость, время выполнения.
    :rtype: (tuple)
    """

    def create_individual() -> np.array:
        """
        Создает индивидуальное решение (матрицу распределения поставок).

        Возвращает:
        :return: Индивидуальное решение.
        :rtype: (np.array)
        """
        individual = np.zeros((num_sources, num_destinations), dtype=int)
        for i in range(num_sources):
            allocated = 0
            for j in range(num_destinations):
                if allocated < supply[i] and np.sum(individual[:, j]) < demand[j]:
                    allocation = min(supply[i] - allocated, demand[j] - np.sum(individual[:, j]))
                    individual[i, j] = allocation
                    allocated += allocation
        return individual

    def fitness(individual) -> float:
        """
        Вычисляет приспособленность (общую стоимость) индивидуального решения.

        :param np.array individual: Индивидуальное решение.

        :return: Общая стоимость решения.
        :rtype: (float)
        """

        total_cost = 0
        for i in range(num_sources):
            for j in range(num_destinations):
                if individual[i, j] > 0:
                    total_cost += individual[i, j] * cost[i, j] + fixed_cost[i, j]
        return total_cost

    def crossover(parent1, parent2) -> np.array:
        """
        Выполняет кроссовер (скрещивание) двух родительских решений для создания потомка.

        :param np.array parent1: Первое родительское решение.
        :param np.array parent2: Второе родительское решение.

        :return: Решение-потомок.
        :rtype np.array
        """
        crossover_point = random.randint(1, num_sources - 1)
        child = np.vstack((parent1[:crossover_point, :], parent2[crossover_point:, :]))
        return child

    def mutate(individual) -> np.array:
        """
        Выполняет мутацию индивидуального решения.

        :param np.array individual: Индивидуальное решение.

        :return: Модифицированное решение.
        :rtype: (np.array)
        """

        if random.random() < mutation_rate:
            i = random.randint(0, num_sources - 1)
            j = random.randint(0, num_destinations - 1)
            k = random.randint(0, num_destinations - 1)
            if j != k and individual[i, j] > 0:
                transfer = random.randint(1, individual[i, j])
                individual[i, j] -= transfer
                individual[i, k] += transfer
        return individual

    def select_parent(population, fitnesses) -> np.array:
        """
        Выбирает родительское решение из популяции с учетом приспособленности.

        :param list population: Популяция решений.
        :param list fitnesses: Список приспособленностей.

        :return: Выбранное родительское решение.
        :rtype: (np.array)
        """

        idx = random.choices(range(population_size), weights=1 / fitnesses, k=1)[0]
        return population[idx]

    start_time = time.time()

    num_sources = len(supply)
    num_destinations = len(demand)

    population = [create_individual() for _ in range(population_size)]
    fitnesses = np.array([fitness(individual) for individual in population])

    for generation in range(max_generations):
        new_population = []
        for _ in range(population_size):
            parent1 = select_parent(population, fitnesses)
            parent2 = select_parent(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        fitnesses = np.array([fitness(individual) for individual in population])

    best_individual = population[np.argmin(fitnesses)]
    best_fitness = min(fitnesses)
    end_time = time.time()

    results = []
    for i in range(num_sources):
        for j in range(num_destinations):
            if best_individual[i, j] > 0:
                total_cost = best_individual[i, j] * cost[i, j] + fixed_cost[i, j]
                results.append((i, j, best_individual[i, j], total_cost))

    execution_time = end_time - start_time

    return results, best_fitness, execution_time


# ToDo: Функция отбора решения
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
        results, fitness, execution_time = genetic_algorithm_transportation(supply, demand, cost, fixed_cost,
                                                                            max_generations, population_size,
                                                                            mutation_rate)
        total_execution_time += execution_time
        if fitness < best_fitness:
            best_fitness = fitness
            best_results = results

    return best_results, best_fitness, total_execution_time


# ToDo: пример работы
if __name__ == '__main__':
    # Пример использования
    supply = [20, 30, 25]
    demand = [10, 15, 20, 30]
    cost = np.array([[8, 6, 10, 9],
                     [9, 12, 13, 7],
                     [14, 9, 16, 5]])
    fixed_cost = np.array([[1, 1, 2, 1],
                           [3, 2, 2, 3],
                           [4, 2, 3, 1]])

    best_results, best_fitness, total_execution_time = find_best_solution(supply, demand, cost, fixed_cost, runs=4)

    print("Оптимальный транспортный план:")
    print("Поставщик -> Потребитель | Размер поставки | стоимость")
    for result in best_results:
        supplier, consumer, amount, cost = result
        print(f"{supplier} -> {consumer} | {amount} | {cost:.2f}")

    print(f"\nОбщая оптимальная стоимость: {best_fitness:.2f}")
    print(f"Время выполнения : {total_execution_time:.2f} секунд")
