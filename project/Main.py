from generation import generate_transportation_data
from algorithm import genetic_algorithm
from dynamic_analog import solve_transportation_problem
from pulp_analog import solve_transportation_problem_pulp


#generate_transportation_data(num_factories=3, num_stores=2)
sol_mas,solut, timer = genetic_algorithm()
print("Работа нашего генетического алгоритма")
print("матрица решения:")
print(sol_mas)
print("счёт:")
print(solut)
print("время работы")
print(timer)
print("___" * 22 )
print('\n')


filename = "data/data_20.txt"

total_cost, elapsed_time = solve_transportation_problem(filename)
print("решение методом динамического программирования")
print(f"File: {filename}, Total Cost: {total_cost}, Elapsed Time: {elapsed_time:.4f} seconds\n")
print("___" * 22 )
print('\n')


status, total_cost, elapsed_time = solve_transportation_problem_pulp(filename)
print("решение библиотеки pulp")
print(f" Total Cost: {total_cost}, Elapsed Time: {elapsed_time:.4f} seconds\n")