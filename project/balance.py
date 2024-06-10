import numpy as np
import copy
from reader import read_transportation_data

def balancing(co_population):
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data()

    new_population = []
    for sol in co_population:
        S = copy.deepcopy(production)
        D = copy.deepcopy(demand)

        for i in range(num_factories):
            S[i] -= np.sum(sol[i])

        for i in range(num_stores):
            sol_1 = np.array(sol)
            D[i] -= np.sum(sol_1[:, i])

        for i in range(len(S)):
            for j in range(len(D)):
                if sol[i][j] != 0:
                    rez = min(S[i], D[j])
                    sol[i][j] += rez
                    S[i] -= rez
                    D[j] -= rez

            for j in range(len(D)):
                sol[i][j] += min(S[i], D[j])
                S[i] -= min(S[i], D[j])
                D[j] -= min(S[i], D[j])

        new_population.append(sol)
    return new_population
