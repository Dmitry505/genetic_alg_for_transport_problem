def read_transportation_data(filename="data/data_20.txt"):

  with open(filename, "r") as f:
    num_factories, num_stores = map(int, f.readline().split())
    f.readline()  # Пропускаем пустую строку

    production = list(map(int, f.readline().split()))
    demand = list(map(int, f.readline().split()))
    f.readline()  # Пропускаем пустую строку

    costs = []
    for _ in range(num_factories):
      costs.append(list(map(int, f.readline().split())))
    f.readline()  # Пропускаем пустую строку

    fixed_costs = []
    for _ in range(num_factories):
      fixed_costs.append(list(map(int, f.readline().split())))

    return num_factories, num_stores, production, demand, costs, fixed_costs
