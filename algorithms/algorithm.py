import numpy as np
import random
from project.reader import read_transportation_data
# необходимо прописать: $env:PYTHONPATH = "c:\Users\zenfo\Desktop\1\vs code\genetic_alg_for_transport_problem" для успешного импортирования метода read_transportation_data

# Функция для инициализации популяции решений
def init_population(pop_size, num_sources, num_destinations):
    population = []
    for _ in range(pop_size):
        individual = np.zeros((num_sources, num_destinations))
        # Случайным образом назначаем каждому источнику магазин назначения
        for i in range(num_sources):
            individual[i] = np.random.permutation(num_destinations)
        population.append(individual)
    return population

# Функция для оценки пригодности индивидуального решения
def evaluate_fitness(individual, costs, fixed_charges):
    total_cost = 0
    for i in range(individual.shape[0]):
        for j in range(individual.shape[1]):
            if individual[i][j] > 0:
                # Добавляем транспортные издержки и фиксированные затраты для каждого назначения
                total_cost += costs[i][j] + fixed_charges[i][j]
    return total_cost

# Функция для выбора родительских решений на основе пригодности
def selection(population, fitnesses, num_parents):
    # Выбираем родителей с вероятностью, пропорциональной их пригодности
    parents = random.choices(population, weights=fitnesses, k=num_parents)
    return parents

# Функция для выполнения кроссовера между двумя родительскими решениями
def crossover(parent1, parent2):
    crossover_point = random.randint(1, parent1.shape[1] - 1)
    # Создаем потомков, объединяя части обоих родителей
    child1 = np.hstack((parent1[:, :crossover_point], parent2[:, crossover_point:]))
    child2 = np.hstack((parent2[:, :crossover_point], parent1[:, crossover_point:]))
    return child1, child2

# Функция для введения мутации в индивидуальное решение
def mutate(individual, mutation_rate):
    for i in range(individual.shape[0]):
        if random.random() < mutation_rate:
            # Обмен двух случайных назначений для каждого источника
            swap_indices = np.random.choice(individual.shape[1], 2, replace=False)
            individual[i][swap_indices[0]], individual[i][swap_indices[1]] = individual[i][swap_indices[1]], individual[i][swap_indices[0]]
    return individual

# Основная функция, реализующая генетический алгоритм
def genetic_algorithm_with_file(file_path, pop_size=100, num_generations=500, mutation_rate=0.01):
    # Читаем транспортные данные из файла
    num_sources, num_destinations, production, demand, costs, fixed_charges = read_transportation_data(file_path)
    costs = np.array(costs)
    fixed_charges = np.array(fixed_charges)
    
    # Инициализируем популяцию решений
    population = init_population(pop_size, num_sources, num_destinations)
    
    # Цикл эволюции
    for generation in range(num_generations):
        # Оцениваем пригодность для каждого индивидуального решения в популяции
        fitnesses = [evaluate_fitness(ind, costs, fixed_charges) for ind in population]
        
        # Выбираем родителей для следующего поколения
        new_population = []
        for _ in range(pop_size // 2):
            parents = selection(population, fitnesses, 2)
            # Выполняем кроссовер для генерации потомков
            child1, child2 = crossover(parents[0], parents[1])
            # Применяем мутацию к потомкам
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
        
        # Заменяем старую популяцию новой
        population = new_population
    
    # Находим лучшее решение в конечной популяции
    best_individual = min(population, key=lambda ind: evaluate_fitness(ind, costs, fixed_charges))
    best_fitness = evaluate_fitness(best_individual, costs, fixed_charges)
    
    return best_individual, best_fitness

# Путь к файлу с транспортными данными
file_path = 'C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/data_10.txt'
# Запускаем генетический алгоритм с указанным файлом
best_solution, best_cost = genetic_algorithm_with_file(file_path)
# Выводим лучшее решение и его стоимость
print("Лучшее решение:")
print(best_solution)
print("Стоимость лучшего решения:")
print(best_cost)
