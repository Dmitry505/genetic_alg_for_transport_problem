from ortools.linear_solver import pywraplp
from project.reader import read_transportation_data

def solve_transportation_problem(filename="transportation_data.txt"):
    # Read data from the file
    num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data(filename)
    
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Define variables
    x = {}
    y = {}
    for i in range(num_factories):
        for j in range(num_stores):
            x[(i, j)] = solver.IntVar(0, solver.infinity(), f'x[{i},{j}]')
            y[(i, j)] = solver.BoolVar(f'y[{i},{j}]')

    # Define constraints
    # Supply constraints
    for i in range(num_factories):
        solver.Add(solver.Sum([x[i, j] for j in range(num_stores)]) <= production[i])

    # Demand constraints
    for j in range(num_stores):
        solver.Add(solver.Sum([x[i, j] for i in range(num_factories)]) >= demand[j])

    # Link x and y variables
    for i in range(num_factories):
        for j in range(num_stores):
            solver.Add(x[(i, j)] <= y[(i, j)] * demand[j])

    # Define the objective function
    objective = solver.Objective()
    for i in range(num_factories):
        for j in range(num_stores):
            objective.SetCoefficient(x[(i, j)], costs[i][j])
            objective.SetCoefficient(y[(i, j)], fixed_costs[i][j])
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        total_cost = 0
        for i in range(num_factories):
            for j in range(num_stores):
                if y[i, j].solution_value() > 0:
                    total_cost += x[i, j].solution_value() * costs[i][j] + fixed_costs[i][j]
                print(f'Ship {x[i, j].solution_value()} units from factory {i} to store {j} with fixed cost {fixed_costs[i][j] * y[i, j].solution_value()}')
        print('Total cost =', total_cost)
    else:
        print('The problem does not have an optimal solution.')

# Example usage
solve_transportation_problem("C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/data_1.txt")
