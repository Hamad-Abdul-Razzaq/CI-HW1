from EA import *


class TSP(EA):
    def __init__(self, hyp):
        super().__init__(hyp)
        lst = []
        with open(self.datapath,"r") as file:
            lst = [i.strip().split() for i in file]
        for _ in range(7):
            lst.pop(0)
        lst.pop(-1)
        lst = [[float(i) for i in j] for j in lst]
        self.distance = [[0 for _ in range(len(lst))] for __ in range(len(lst))]
        for i in range(len(lst)):
            for j in range(i+1,len(lst)):
                self.distance[i][j] = self.distance[j][i] = ((lst[i][1] - lst[j][1])**2 + (lst[i][2] - lst[j][2])**2)**(1/2)
    
    def initialize(self) -> None:
        for _ in range(self.population_size):
            p = [i for i in range(len(self.distance))]
            np.random.shuffle(p)
            self.Population.append(p)

    def fitness(self, p):
        fitness_val = 0
        for i in range(len(p)-1):
            fitness_val += self.distance[p[i]][p[i+1]]
        return fitness_val
    
    def CrossOver(self):
        for i in range(0,len(self.Parents)-1, 2):
            parent1 = self.Parents[i].copy()
            parent2 = self.Parents[i + 1].copy()
            offspring = [-1 for _ in range(len(parent1))]
            idx = random.randint(0,len(parent1)//2)
            offspring[idx: idx + len(parent1)//2] = parent1[idx:idx + len(parent1)//2]
            c = 0
            for j in range( len(parent2)):
                if c == idx:
                    c = idx + len(parent2)//2
                if not(parent2[j] in offspring):
                    offspring[c] = parent2[j]
                    c += 1
            self.OffSprings.append(offspring)
    def Mutation(self) -> None:
        for i in range(self.offspring_size):
            rnd1 = random.randint(0,len(self.OffSprings[i]) - 1)
            rnd2 = random.randint(0,len(self.OffSprings[i]) - 1)
            while rnd2 == rnd1:
                rnd2 = random.randint(0,len(self.OffSprings[i]) - 1)
            if rnd1 < rnd2:
                self.OffSprings[i] = self.OffSprings[i][:rnd1+1] + [self.OffSprings[i][rnd2]] + self.OffSprings[i][rnd1+1:rnd2] + self.OffSprings[i][rnd2+1:]
            else:
                self.OffSprings[i] = self.OffSprings[i][:rnd2+1] + [self.OffSprings[i][rnd1]] + self.OffSprings[i][rnd2+1:rnd1] + self.OffSprings[i][rnd1+1:]

        
    
    


