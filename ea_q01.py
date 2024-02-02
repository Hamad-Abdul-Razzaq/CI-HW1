from gettext import find
import numpy as np
import random

distance = []
with open ("distance.txt", "r") as file:
    distance = [[float(j) for j in i.strip().split()] for i in file]


# Fitness Function
def fitness(p):
    fitness_val = 0
    for i in range(len(p)-1):
        fitness_val += distance[p[i]][p[i+1]]
    return fitness_val

# Selection Procedure
def selection_procedure(fit_val: list, population: list, procedure: str, size):
    if procedure == 'Truncation':
        idx_lst = np.argsort(fit_val)
        return [population[idx_lst[i]] for i in range(size)]


# Crossover
def crossover(parents):
    offsprings = list()
    for i in range(0,len(parents)-1, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        offspring = [-1 for _ in range(len(parent1))]
        idx = random.randint(0,len(parent1)//2)
        offspring[idx: idx + len(parent1)//2] = parent1[idx:idx + len(parent1)//2]
        c = 0
        for j in range( len(parent2)):
            # print(c, j)
            if c == idx:
                c = idx + len(parent2)//2
            if not(parent2[j] in offspring):
                offspring[c] = parent2[j]
                c += 1
        offsprings.append(offspring)
    return offsprings

# Mutation
def mutation(offsprings):
    for i in range(len(offsprings)):
        rnd1 = random.randint(0,len(offsprings[i]) - 1)
        rnd2 = random.randint(0,len(offsprings[i]) - 1)
        while rnd2 == rnd1:
            rnd2 = random.randint(0,len(offsprings[i]) - 1)
        if rnd1 < rnd2:
            offsprings[i] = offsprings[i][:rnd1+1] + [offsprings[i][rnd2]] + offsprings[i][rnd1+1:rnd2] + offsprings[i][rnd2+1:]
        else:
            offsprings[i] = offsprings[i][:rnd2+1] + [offsprings[i][rnd1]] + offsprings[i][rnd2+1:rnd1] + offsprings[i][rnd1+1:]


population_size = 30
offspring_size = 10
num_generations = 50
mutation_rate = 0.5
iterations = 20000

# Initializing Population
Population = list()
min_so_far = float('inf')
for _ in range(population_size):
    p = [i for i in range(len(distance))]
    np.random.shuffle(p)
    Population.append(p)
iter = 0
while iter < iterations:
    fitness_values = []
    for i in Population:
        fitness_values.append(fitness(i))
    parents = selection_procedure(fitness_values, Population, 'Truncation', offspring_size*2)
        
        
    offsprings = crossover(parents)
    mutation(offsprings)
    TotalPopulation = Population + offsprings
    for i in offsprings:
        fitness_values.append(fitness(i))
    Population = selection_procedure(fitness_values, TotalPopulation, 'Truncation', population_size)
    iter += 1
    # if min(fitness_values) < min_so_far:
    #     min_so_far = min(fitness_values)
    #     min_so_far_idx = fitness_values.index(min(fitness_values))
    print(min(fitness_values))
# print(Population[min_so_far_idx])


