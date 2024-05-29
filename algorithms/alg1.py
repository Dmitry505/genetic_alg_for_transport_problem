import numpy as np
import random

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Чтение размеров
    num_sources, num_destinations = map(int, lines[0].split())

    # Чтение матрицы затрат
    costs = []
    for i in range(1, num_sources + 1):
        costs.append(list(map(int, lines[i].split())))
    costs = np.array(costs)

    # Чтение фиксированных доплат
    fixed_charges = []
    for i in range(num_sources + 1, num_sources + num_sources + 1):
        fixed_charges.append(list(map(int, lines[i].split())))
    fixed_charges = np.array(fixed_charges)

    return costs, fixed_charges

def init_population(pop_size, num_sources, num_destinations):
    population = []
    for _ in range(pop_size):
        individual = np.zeros((num_sources, num_destinations))
        for i in range(num_sources):
            individual[i] = np.random.permutation(num_destinations)
        population.append(individual)
    return population

def evaluate_fitness(individual, costs, fixed_charges):
    total_cost = 0
    for i in range(individual.shape[0]):
        for j in range(individual.shape[1]):
            if individual[i][j] > 0:
                total_cost += costs[i][j] + fixed_charges[i][j]
    return total_cost

def selection(population, fitnesses, num_parents):
    parents = random.choices(population, weights=fitnesses, k=num_parents)
    return parents

def crossover(parent1, parent2):
    crossover_point = random.randint(1, parent1.shape[1] - 1)
    child1 = np.hstack((parent1[:, :crossover_point], parent2[:, crossover_point:]))
    child2 = np.hstack((parent2[:, :crossover_point], parent1[:, crossover_point:]))
    return child1, child2

def mutate(individual, mutation_rate):
    for i in range(individual.shape[0]):
        if random.random() < mutation_rate:
            swap_indices = np.random.choice(individual.shape[1], 2, replace=False)
            individual[i][swap_indices[0]], individual[i][swap_indices[1]] = individual[i][swap_indices[1]], individual[i][swap_indices[0]]
    return individual

def genetic_algorithm_with_file(file_path, pop_size=100, num_generations=500, mutation_rate=0.01):
    costs, fixed_charges = read_data(file_path)
    num_sources, num_destinations = costs.shape
    population = init_population(pop_size, num_sources, num_destinations)
    
    for generation in range(num_generations):
        fitnesses = [evaluate_fitness(ind, costs, fixed_charges) for ind in population]
        
        new_population = []
        for _ in range(pop_size // 2):
            parents = selection(population, fitnesses, 2)
            child1, child2 = crossover(parents[0], parents[1])
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
        
        population = new_population
    
    best_individual = min(population, key=lambda ind: evaluate_fitness(ind, costs, fixed_charges))
    best_fitness = evaluate_fitness(best_individual, costs, fixed_charges)
    
    return best_individual, best_fitness

file_path = '/mnt/data/data_1.txt'
best_solution, best_cost = genetic_algorithm_with_file(file_path)
print("Лучшее решение:")
print(best_solution)
print("Затраты на лучшее решение:")
print(best_cost)
