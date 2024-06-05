from reader import read_transportation_data
import numpy as np
from math import ceil

def solution(sol):
    fin = 0
    for i in range (num_factories):
        for j in range(num_stores):
            if sol[i][j] != 0:
                fin += sol[i][j] * costs[i][j]
                fin += fixed_costs[i][j]

    for i in range(num_factories):
        sum_production = 0
        for j in range(num_stores):
            sum_production += sol[i][j]
        if (sum_production > production[i]):
            fin += np.sum(demand) * 5

    if (np.sum(sol) < np.sum(demand)//2):
        fin += np.sum(demand) * 10

    if (np.sum(sol) != np.sum(demand)):
        fin = ceil(1.1 * fin)
        fin += ceil((1 + ((1 - np.sum(sol)//np.sum(demand)) * 50)**2//100) * fin)
    return fin

num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data()

