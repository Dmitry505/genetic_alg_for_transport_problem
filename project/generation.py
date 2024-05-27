import random
from math import ceil

def generate_transportation_data(num_factories, num_stores, filename="transportation_data.txt"):

    demand = [random.randint(40, 150) for _ in range(num_stores)]
    s_demand = ''
    sum = 0
    for i in demand:
        s_demand += str(i) + " "
        sum += i


    distribution = ceil(sum//num_factories * 1.25)
    min_dis = ceil(distribution * 0.6)
    max_dis = ceil(distribution * 1.5)
    production = [random.randint(min_dis, max_dis) for _ in range(num_factories)]
    sum_prod = 0
    for i in production:
        sum_prod += i
    if (sum_prod < ceil(sum * 1.25)):
        addition = ceil(sum * 1.25 - sum_prod)
        add_dis = addition//num_factories + num_factories
        for i in range(len(production)):
            production[i] +=  add_dis
    s_production = ''
    for i in production:
        s_production += str(i) + " "

    costs = [[random.randint(2, 10) for _ in range(num_stores)] for _ in range(num_factories)]

    fixed_costs = [[random.randint(30, 70) for _ in range(num_stores)] for _ in range(num_factories)]


    with open(filename, "w") as f:

        f.write(f"{num_factories} {num_stores}\n")
        f.write("\n")

        f.write(s_production)
        f.write("\n")

        f.write(s_demand)
        f.write("\n")
        f.write("\n")

        s_costs = ''
        for i in range(num_factories):
            for j in range(num_stores):
                s_costs += str(costs[i][j]) + " "
            f.write(s_costs)
            f.write("\n")
            s_costs = ''
        f.write("\n")

        s_fixed_costs = ''
        for i in range(num_factories):
            for j in range(num_stores):
                s_fixed_costs += str(fixed_costs[i][j]) + " "
            f.write(s_fixed_costs)
            f.write("\n")
            s_fixed_costs = ''