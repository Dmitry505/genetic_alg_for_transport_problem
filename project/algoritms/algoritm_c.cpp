#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <limits>
#include <sstream>
#include <tuple>

using namespace std;

default_random_engine generator(chrono::system_clock::now().time_since_epoch().count());

struct TransportPlan {
    int supplier;
    int consumer;
    int amount;
    double cost;
};

vector<vector<int>> create_individual(const vector<int>& supply, const vector<int>& demand) {
    int num_sources = supply.size();
    int num_destinations = demand.size();
    vector<vector<int>> individual(num_sources, vector<int>(num_destinations, 0));
    for (int i = 0; i < num_sources; ++i) {
        int allocated = 0;
        for (int j = 0; j < num_destinations; ++j) {
            if (allocated < supply[i] && accumulate(individual.begin(), individual.end(), 0,
                [&](int sum, const vector<int>& ind) { return sum + ind[j]; }) < demand[j]) {
                int allocation = min(supply[i] - allocated, demand[j] -
                    accumulate(individual.begin(), individual.end(), 0, [&](int sum, const vector<int>& ind) { return sum + ind[j]; }));
                individual[i][j] = allocation;
                allocated += allocation;
            }
        }
    }
    return individual;
}

double fitness(const vector<vector<int>>& individual, const vector<vector<double>>& cost, const vector<vector<double>>& fixed_cost) {
    double total_cost = 0.0;
    for (size_t i = 0; i < individual.size(); ++i) {
        for (size_t j = 0; j < individual[i].size(); ++j) {
            if (individual[i][j] > 0) {
                total_cost += individual[i][j] * cost[i][j] + fixed_cost[i][j];
            }
        }
    }
    return total_cost;
}

vector<vector<int>> crossover(const vector<vector<int>>& parent1, const vector<vector<int>>& parent2) {
    int crossover_point = uniform_int_distribution<int>(1, parent1.size() - 1)(generator);
    vector<vector<int>> child(parent1.size(), vector<int>(parent1[0].size()));
    copy(parent1.begin(), parent1.begin() + crossover_point, child.begin());
    copy(parent2.begin() + crossover_point, parent2.end(), child.begin() + crossover_point);
    return child;
}

void mutate(vector<vector<int>>& individual, double mutation_rate) {
    uniform_real_distribution<double> distribution(0.0, 1.0);
    if (distribution(generator) < mutation_rate) {
        int i = uniform_int_distribution<int>(0, individual.size() - 1)(generator);
        int j = uniform_int_distribution<int>(0, individual[i].size() - 1)(generator);
        int k = uniform_int_distribution<int>(0, individual[i].size() - 1)(generator);
        if (j != k && individual[i][j] > 0) {
            int transfer = uniform_int_distribution<int>(1, individual[i][j])(generator);
            individual[i][j] -= transfer;
            individual[i][k] += transfer;
        }
    }
}

vector<vector<int>> select_parent(const vector<vector<vector<int>>>& population, const vector<double>& fitnesses) {
    discrete_distribution<int> distribution(fitnesses.begin(), fitnesses.end());
    return population[distribution(generator)];
}

tuple<vector<TransportPlan>, double, double> genetic_algorithm_transportation(const vector<int>& supply, const vector<int>& demand, const vector<vector<double>>& cost, const vector<vector<double>>& fixed_cost, int max_generations, int population_size, double mutation_rate) {
    int num_sources = supply.size();
    int num_destinations = demand.size();

    auto start_time = chrono::high_resolution_clock::now();

    vector<vector<vector<int>>> population;
    for (int i = 0; i < population_size; ++i) {
        population.push_back(create_individual(supply, demand));
    }
    vector<double> fitnesses(population_size);
    transform(population.begin(), population.end(), fitnesses.begin(), [&](const vector<vector<int>>& individual) { return fitness(individual, cost, fixed_cost); });

    for (int generation = 0; generation < max_generations; ++generation) {
        vector<vector<vector<int>>> new_population;
        for (int i = 0; i < population_size; ++i) {
            vector<vector<int>> parent1 = select_parent(population, fitnesses);
            vector<vector<int>> parent2 = select_parent(population, fitnesses);
            vector<vector<int>> child = crossover(parent1, parent2);
            mutate(child, mutation_rate);
            new_population.push_back(child);
        }
        population = move(new_population);
        transform(population.begin(), population.end(), fitnesses.begin(), [&](const vector<vector<int>>& individual) { return fitness(individual, cost, fixed_cost); });
    }

    auto min_it = min_element(fitnesses.begin(), fitnesses.end());
    int best_index = distance(fitnesses.begin(), min_it);
    double best_fitness = *min_it;

    vector<TransportPlan> best_plan;
    for (int i = 0; i < num_sources; ++i) {
        for (int j = 0; j < num_destinations; ++j) {
            if (population[best_index][i][j] > 0) {
                best_plan.push_back({i, j, population[best_index][i][j], population[best_index][i][j] * cost[i][j] + fixed_cost[i][j]});
            }
        }
    }

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> execution_time = end_time - start_time;

    return make_tuple(best_plan, best_fitness, execution_time.count());
}

vector<int> parse_vector(const string& str) {
    vector<int> result;
    stringstream ss(str);
    string item;
    while (getline(ss, item, ',')) {
        result.push_back(stoi(item));
    }
    return result;
}

vector<vector<double>> parse_matrix(const string& str, int rows, int cols) {
    vector<vector<double>> result(rows, vector<double>(cols));
    stringstream ss(str);
    string item;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            if (!getline(ss, item, ',')) {
                throw runtime_error("Error parsing matrix");
            }
            result[i][j] = stod(item);
        }
    }
    return result;
}

int main(int argc, char* argv[]) {
    if (argc != 8) {
        cerr << "Usage: " << argv[0] << " supply demand cost fixed_cost max_generations population_size mutation_rate" << endl;
        return 1;
    }

    vector<int> supply = parse_vector(argv[1]);
    vector<int> demand = parse_vector(argv[2]);
    int num_sources = supply.size();
    int num_destinations = demand.size();
    vector<vector<double>> cost = parse_matrix(argv[3], num_sources, num_destinations);
    vector<vector<double>> fixed_cost = parse_matrix(argv[4], num_sources, num_destinations);
    int max_generations = stoi(argv[5]);
    int population_size = stoi(argv[6]);
    double mutation_rate = stod(argv[7]);

    vector<TransportPlan> results;
    double best_fitness, execution_time;
    tie(results, best_fitness, execution_time) = genetic_algorithm_transportation(supply, demand, cost, fixed_cost, max_generations, population_size, mutation_rate);

    cout << best_fitness << " " << execution_time << " ";
    for (const auto& result : results) {
        cout << result.supplier << " " << result.consumer << " " << result.amount << " " << result.cost << " ";
    }
    cout << endl; // Добавляем символ новой строки в конце вывода для правильного разбора
    return 0;
}
