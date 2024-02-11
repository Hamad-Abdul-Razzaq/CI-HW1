import numpy as np
import random
from math import log10

class EA:
    def __init__(self, hyp) -> None:
        self.iterations = hyp['Iterations']
        self.generations = hyp['Generations']
        self.population_size = hyp['Population Size']
        self.offspring_size = hyp['OffSpring Size']
        self.mutation_rate = hyp['Mutation Rate']
        self.Population = []
        self.OffSprings = []
        self.Parents = []
        self.fit_lst = []
        self.parent_p = hyp['Parent Procedure']
        self.survival_p = hyp['Survival Procedure']
        self.tournament_size = hyp['Tournament Size']
        self.current_generation = 0
        self.current_iteration = 0


    def initialize(self) -> None:
        pass

    def selection(self, procedure, tournament_size, size) -> None:
        if procedure == 'Truncation':
            idx_lst = np.argsort(self.fit_lst)
            return [self.Population[idx_lst[i]].copy() for i in range(size)]
        elif procedure == 'TS':
            Tsample_idx = [random.randint(0,len(self.Population)-1) for i in range(tournament_size)]
            Tsample = [self.Population[Tsample_idx[i]] for i in range(len(Tsample_idx))]
            fitness_vals = [self.fit_lst[Tsample_idx[i]] for i in range(len(Tsample_idx))]
            idx_lst = np.argsort(fitness_vals)
            return [Tsample[idx_lst[i]] for i in range(size)]
        elif procedure == 'Rank Selection':
            idx_lst = np.argsort(fit_val)
            descending_population = [self.Population[idx_lst[i]] for i in range(len(idx_lst)-1,-1,-1)]
            rangeDict = {i: ((i*(i-1)/2*3000/len(self.Population)), ((i)*(i+1)/2*3000/len(self.Population))) for i in range(1,len(self.Population) + 1)}
            selected = []
            minVal = 0
            maxVal = len(self.Population)*(len(self.Population)+1)/2*3000/len(self.Population)
            selectedVals = [random.randint(minVal,maxVal) for i in range(size)]
            for i in range(len(selectedVals)):
                for j in rangeDict:
                    if rangeDict[j][0] <= selectedVals[i] < rangeDict[j][1]:
                        selected.append(descending_population[j - 1])
            return selected
        elif procedure == 'Fitness Prop':
            probs = [1/(log10(log10(i))) for i in self.fit_lst]
            normprob = [i/sum(probs) for i in probs]
            rangeDict = list()
            prev = None
            for i in range(len(normprob)):
                if i == 0:
                    rangeDict.append((0,normprob[i]*3000))
                    prev = normprob[i]*3000
                else:
                    rangeDict.append((prev, prev + normprob[i]*3000))
                    prev = prev + normprob[i]*3000
            selected = []
            selectedVals = [random.randint(0,3000) for i in range(size)]
            for i in range(len(selectedVals)):
                c = 0
                inserted = False
                for j in range(len(rangeDict)):
                    if rangeDict[j][0] <= selectedVals[i] <= rangeDict[j][1]:
                        selected.append(self.Population[c])
                        inserted = True
                if not(inserted):
                    print(selectedVals[i])
                    c += 1
            return selected
    
    def Iteration(self) -> None:
        self.Population = list()
        self.current_generation = 0
        self.initialize()
        while self.current_generation < self.generations:
            self.fit_lst = list()
            self.EvaluateFitness('P')
            print('Fitness', self.fit_lst)
            # print("Before 1", len(self.Population))
            self.Parents = self.selection(self.parent_p, self.tournament_size, self.offspring_size*2)
            # print("After 1", len(self.Population))
            self.CrossOver()
            self.Mutation()
            self.EvaluateFitness('O')
            self.Population.extend(self.OffSprings)
            # print("Before 2", len(self.Population))
            self.Population = self.selection(self.survival_p, self.tournament_size, self.population_size).copy()
            # print("After 2", len(self.Population))
            self.current_generation += 1
            self.DisplayGenerationInfo()
    
    def Simulate(self) -> None:
        self.current_iteration = 0
        while self.current_iteration < self.iterations:
            self.Iteration()
            self.current_iteration += 1
            self.DisplayIterationInfo()

    def Mutation(self) -> None:
        pass

    def CrossOver(self, parents) -> None:
        pass

    def fitness(self, p):
        pass

    def EvaluateFitness(self, r) -> None:
        if r == 'P':
            for i in self.Population:
                print(self.fitness(i))
                self.fit_lst.append(self.fitness(i))
        elif r == 'O':
            for i in self.OffSprings:
                self.fit_lst.append(self.fitness(i))

    def DisplayGenerationInfo(self) -> None:
        print("Current Generation:", self.current_generation)
        print("Optimal Fitness Value So Far:", min(self.fit_lst))
    def DisplayIterationInfo(self) -> None:
        print("Current Iteration:", self.current_iteration)



