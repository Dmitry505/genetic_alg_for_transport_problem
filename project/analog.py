import random
import pulp
from reader import read_transportation_data

def solve_transportation_problem(filename="transportation_data.txt"):
    # Create the LP problem
    prob = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

    # Define variables
    x = pulp.LpVariable.dicts("x", [(i, j) for i in range(num_factories) for j in range(num_stores)], lowBound=0, cat='Integer')

    # Objective function: minimize total cost
    prob += pulp.lpSum([costs[i][j] * x[(i, j)] for i in range(num_factories) for j in range(num_stores)]) + \
            pulp.lpSum(
                [fixed_costs[i][j] * pulp.lpSum(x[(i, j)]) for i in range(num_factories) for j in range(num_stores)])

    # Constraints:
    # 1. Supply constraints (production)в
    for i in range(num_factories):
        prob += pulp.lpSum([x[(i, j)] for j in range(num_stores)]) <= production[i]

    # 2. Demand constraints
    for j in range(num_stores):
        prob += pulp.lpSum([x[(i, j)] for i in range(num_factories)]) == demand[j] # Изменено на == для точного равенства спросу

    # Solve the problem
    prob.solve()

    # Print the solution
    print("Status:", pulp.LpStatus[prob.status])
    print("Total Cost:", pulp.value(prob.objective))
    print("\nTransportation Schedule:")
    for i in range(num_factories):
        for j in range(num_stores):
            if x[(i, j)].varValue > 0:
                print(f"Factory {i+1} -> Store {j+1}: {x[(i, j)].varValue}")

num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data()
solve_transportation_problem()
