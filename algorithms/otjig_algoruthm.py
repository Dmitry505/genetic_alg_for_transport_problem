import numpy as np
from simanneal import Annealer
from itertools import product
from project.reader import read_transportation_data

class TransportationProblem(Annealer):
    def __init__(self, state, num_factories, num_stores, production, demand, costs, fixed_costs):
        self.num_factories = num_factories
        self.num_stores = num_stores
        self.production = production
        self.demand = demand
        self.costs = costs
        self.fixed_costs = fixed_costs
        super(TransportationProblem, self).__init__(state)  # Инициализация Annealer

    def move(self):
        # Применяем случайное перемещение к одной из фабрик
        i = np.random.randint(self.num_factories)
        self.state[i] = np.random.randint(self.num_stores)

    def energy(self):
        total_cost = 0
        for i, j in product(range(self.num_factories), range(self.num_stores)):
            # Вычисляем затраты на перевозку
            total_cost += self.state[i] == j * (self.costs[i][j] + self.fixed_costs[i][j])
        
        # Учитываем фиксированные доплаты
        for i in range(self.num_factories):
            total_cost += self.fixed_costs[i][self.state[i]]
        
        return total_cost

# Чтение данных
num_factories, num_stores, production, demand, costs, fixed_costs = read_transportation_data("C:/Users/zenfo/Desktop/1/vs code/genetic_alg_for_transport_problem/data/data_1.txt")
    
# Начальное состояние - распределение производства по складам
initial_state = np.zeros(num_factories, dtype=int)

# Создание объекта задачи
tsp = TransportationProblem(initial_state, num_factories, num_stores, production, demand, costs, fixed_costs)

# Запуск алгоритма отжига
tsp.set_schedule(tsp.auto(minutes=0.2))
state, energy = tsp.anneal()

# Вывод результатов
print("Optimal state:", state)
print("Optimal energy:", energy)
