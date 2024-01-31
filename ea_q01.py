import numpy as np

distance = []
with open ("distance.txt", "r") as file:
    distance = [[float(j) for j in i.strip().split()] for i in file]


# Fitness Function
def fitness(p):
    fitness_val = 0
    for i in range(len(p)-1):
        fitness_val += distance[p[i]][p[i+1]]
    return fitness_val


population_size = 30
offspring_size = 10
num_generations = 50
mutation_rate = 0.5
iterations = 10

# Initializing Population
Population = list()
for _ in range(population_size):
    p = [i for i in range(len(distance))]
    np.random.shuffle(p)
    Population.append(p)
iter = 0
while iter < iterations:
    fitness_values = []
    for i in Population:
        fitness_values.append(fitness(i))
    print(fitness_values)
    break
    iter += 1
