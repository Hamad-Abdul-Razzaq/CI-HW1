import numpy as np
import random
from math import log10
import matplotlib.pyplot as plt

class EA:
    def __init__(self, hyp) -> None:
        self.iterations = hyp['Iterations']
        self.generations = hyp['Generations']
        self.population_size = hyp['Population Size']
        self.offspring_size = hyp['OffSpring Size']
        self.mutation_rate = hyp['Mutation Rate']
        self.datapath = hyp['Data Path']
        self.Population = list()
        self.OffSprings = list()
        self.Parents = list()
        self.fit_lst = list()
        self.Total = list()
        self.parent_p = hyp['Parent Procedure']
        self.survival_p = hyp['Survival Procedure']
        self.tournament_size = hyp['Tournament Size']
        self.current_generation = 0
        self.current_iteration = 0
        self.IterationInfo = dict()


    def initialize(self) -> None:
        pass

    def selection(self, procedure, size, Pop) -> None:
        if procedure == 'Truncation':
            idx_lst = np.argsort(self.fit_lst)
            return [Pop[idx_lst[i]].copy() for i in range(size)]
        elif procedure == 'Tournament Selection':
            Tsample_idx = [random.randint(0,len(Pop)-1) for i in range(self.tournament_size)]
            Tsample = [Pop[Tsample_idx[i]] for i in range(len(Tsample_idx))]
            fitness_vals = [self.fit_lst[Tsample_idx[i]] for i in range(len(Tsample_idx))]
            idx_lst = np.argsort(fitness_vals)
            return [Tsample[idx_lst[i]] for i in range(size)]
        elif procedure == 'Rank Selection':
            idx_lst = np.argsort(self.fit_lst)
            descending_population = [Pop[idx_lst[i]] for i in range(len(idx_lst)-1,-1,-1)]
            rangeDict = {i: ((i*(i-1)/2/len(Pop)), ((i)*(i+1)/2/len(Pop))) for i in range(1,len(Pop) + 1)}
            selected = []
            minVal = 0
            maxVal = len(Pop)*(len(Pop)+1)/2/len(Pop)
            selectedVals = [random.randint(int(minVal*100),int(maxVal*100))//100 for i in range(size)]
            for i in range(len(selectedVals)):
                for j in rangeDict:
                    if rangeDict[j][0] <= selectedVals[i] < rangeDict[j][1]:
                        selected.append(descending_population[j - 1])
            return selected
        elif procedure == 'Fitness Proportional':
            norm = [i/sum(self.fit_lst) for i in self.fit_lst]
            cdf = list()
            selected = list()
            s = 0
            for i in range(len(norm)):
                s += norm[i]
                cdf.append(s)
            rnds = [random.uniform(0,1) for _ in range(size)]
            for x in rnds:
                for i in range(len(cdf)):
                    if x  <= cdf[i]:
                        selected.append(Pop[i])
                        break
            return selected
        elif procedure == 'Random':
            idx_lst = [random.randint(0,len(Pop)-1) for _ in range(size)]
            return [Pop[idx_lst[i]].copy() for i in range(size)]



    
    def Iteration(self) -> None:
        self.Population = list()
        self.current_generation = 0
        self.initialize()
        while self.current_generation < self.generations:
            self.fit_lst = list()
            self.OffSprings = list()
            self.EvaluateFitness('P')
            # print('Fitness', self.fit_lst)
            # print(self.Population)
            # print("Before 1", len(self.Population))
            self.Parents = self.selection(self.parent_p, self.offspring_size*2, self.Population)
            
            # print("After 1", len(self.Population))
            # print(self.fit_lst)
            
            self.CrossOver()

            # print(self.OffSprings)
            
            self.Mutation()
            
            self.EvaluateFitness('O')
            # print(self.fit_lst)
            
            self.Total = self.Population + self.OffSprings
            self.Total = self.Total.copy()
            
            # print("Before 2", len(self.Population))
            Next_Gen = self.selection(self.survival_p, self.population_size, self.Total).copy()
            self.Population = Next_Gen.copy()
            # print("After 2", len(self.Population))
            self.current_generation += 1
            self.DisplayGenerationInfo()
            self.IterationInfo[self.current_iteration][0].append(min(self.fit_lst))
            if (self.IterationInfo[self.current_iteration][0][-1]) < self.IterationInfo[self.current_iteration][2]:
                self.IterationInfo[self.current_iteration][2] = self.IterationInfo[self.current_iteration][0][-1]
                temp_lst = np.argsort(self.fit_lst[0:self.population_size])
                self.IterationInfo[self.current_iteration][3] = self.Population[temp_lst[0]].copy()

            self.IterationInfo[self.current_iteration][1].append(sum(self.fit_lst)/len(self.fit_lst))
    
    def Simulate(self) -> None:
        self.current_iteration = 0
        while self.current_iteration < self.iterations:
            self.IterationInfo[self.current_iteration] = [list(), list(), float('inf'), None]
            self.Iteration()
            self.current_iteration += 1
            self.DisplayIterationInfo()
        self.DisplayResults()
        self.OutputData()
        self.PlotResults()


    def PlotResults(self):
        ABSF = [0 for _ in range(self.generations)]
        AASF = [0 for _ in range(self.generations)]
        for i in self.IterationInfo:
            for j in range(self.generations):
                ABSF[j] += self.IterationInfo[i][0][j]
                AASF[j] += self.IterationInfo[i][1][j]
        ABSF = [i/self.iterations for i in ABSF]
        AASF = [i/self.iterations for i in AASF]
        plt.plot(range(1,self.generations+1),ABSF)
        plt.plot(range(1,self.generations+1),AASF)
        plt.legend(["BSF", "ASF"])
        plt.title("ABSF and AASF")
        plt.xlabel("Generation Number")
        plt.ylabel("Fitness Value")
        plt.show()


    def OutputData(self):
        with open("TSP.txt", "w") as file:
            file.write(str(self.IterationInfo))

    def DisplayResults(self):
        optimal = float('inf')
        optimal_sol = None
        for i in self.IterationInfo.values():
            if i[2] < optimal:
                optimal = i[2]
                optimal_sol = i[3].copy()
        print("Optimal Value:", optimal)
        print("Optimal Solution:", optimal_sol)

    def Mutation(self) -> None:
        pass

    def CrossOver(self) -> None:
        pass

    def fitness(self, p):
        pass

    def EvaluateFitness(self, r) -> None:
        if r == 'P':
            for i in self.Population:
                # print(self.fitness(i))
                self.fit_lst.append(self.fitness(i))
        elif r == 'O':
            for i in self.OffSprings:
                # print(self.fitness(i))
                self.fit_lst.append(self.fitness(i))

    def DisplayGenerationInfo(self) -> None:
        print("Current Generation:", self.current_generation)
        print("Optimal Fitness Value So Far:", min(self.fit_lst))

    def DisplayIterationInfo(self) -> None:
        print("Current Iteration:", self.current_iteration)



