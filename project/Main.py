from reader import read_transportation_data
from generation import generate_transportation_data


generate_transportation_data(num_factories=5, num_stores=4)
num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data()