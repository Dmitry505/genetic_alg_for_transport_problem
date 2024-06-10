import random
import numpy as np
import time
from reader import read_transportation_data
from solution import solution
from balance import balancing


def genetic_algorithm():
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data()

    start_time = time.time()
    population_size = 8
    population_start_size = 64
    mutation_rate = 0.1
    max_generations = 50

    def initialize_population():
        population = []
        for _ in range(population_start_size):
            S = production.copy()
            D = demand.copy()
            chromosome = np.zeros((len(S), len(D)))
            for i in range(len(S)):
                for j in range(len(D)):
                    if random.random() < 0.5:
                        chromosome[i][j] = min(S[i], D[j])
                        S[i] -= chromosome[i][j]
                        D[j] -= chromosome[i][j]
            population.append(chromosome)
        np.unique(population, axis=0)
        return additional_initialization(population)


    def additional_initialization(population):
        if (len(population) < population_size):
            for _ in range(population_size):
                S = production.copy()
                D = demand.copy()
                chromosome = np.zeros((len(S), len(D)))
                for i in range(len(S)):
                    for j in range(len(D)):
                        std = random.randint(0,min(S[i], D[j]))
                        chromosome[i][j] = std
                        S[i] -= chromosome[i][j]
                        D[j] -= chromosome[i][j]
                population.append(chromosome)
        return population

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        return child1, child2

    def mutate(chromosome, mutation_rate):
        for i in range(len(chromosome)):
            for j in range(len(chromosome[0])):
                if random.random() < mutation_rate:
                    not_relz_prod = production[i] - np.sum(chromosome[i]) + chromosome[i][j]
                    not_relz_demand = demand[j] - np.sum(chromosome[:, j]) + chromosome[i][j]
                    chromosome[i][j] = random.choice([0, max(0, min(not_relz_prod, not_relz_demand))])
        return chromosome

    def selection(population):
        population = np.unique(population, axis=0)
        population = sorted(population, key=solution)
        return population[:population_size]

    def score(sol):
        fin = 0
        for i in range(num_factories):
            for j in range(num_stores):
                if (sol[i][j] != 0):
                    fin += sol[i][j] * costs[i][j]
                    fin += fixed_costs[i][j]
        return  fin


    population = initialize_population()
    population = selection(population)
    if (np.sum(population[0]) != np.sum(demand)) :
        population = initialize_population()
        population = selection(population)

    counter = 0
    while(True):
        counter += 1
        l = len(population)
        for i in range (l):
            for j in range (l):
                if (i != j):
                    child1, child2 = crossover(population[i], population[j])
                    child1 = mutate(child1,mutation_rate)
                    child2 = mutate(child2, mutation_rate)
                    population.append(child1)
                    population.append(child2)

        population = selection(population)

        if (counter == max_generations ):
            break



    if (np.sum(population[0]) != np.sum(demand)):
        population = balancing(population)

    fin = score(population[0])

    execution_time = time.time() - start_time

    return population[0],fin,execution_time
