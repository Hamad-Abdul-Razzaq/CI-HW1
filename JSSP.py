from EA import *
import numpy as np

class JSSP(EA):
    def __init__(self, hyp) -> None:
        super().__init__(hyp)
        self.Jobs = dict()
        with open(self.datapath, "r") as file:
            lst = [[int(j) for j in i.strip().split()] for i in file]
            self.J = lst[0][0]
            self.M = lst[0][1]
            for i in range(1,len(lst)):
                self.Jobs[i-1] = list()
                for j in range(0,len(lst[i]),2):
                    self.Jobs[i-1].append((lst[i][j], lst[i][j+1]))

    def initialize(self) -> None:
        self.Population = list()
        for _ in range(self.population_size):
            chromosome = list()
            for i in range(self.J):
                for j in range(self.M):
                    chromosome.append(i)
            np.random.shuffle(chromosome)
            self.Population.append(chromosome)
        
    
    def fitness(self, p):
        current_operation = [0 for _ in range(self.J)]
        prev_operation_time = [0 for _ in range(self.J)]
        machine_time = [0 for _ in range(self.M)]
        for j in p:
            o = current_operation[j]
            m = self.Jobs[j][o][0]
            duration = self.Jobs[j][o][1]
            machine_time[m] = max(machine_time[m], prev_operation_time[j]) + duration
            prev_operation_time[j] = machine_time[m]
            current_operation[j] += 1
        return(max(machine_time))

        

    def CrossOver(self):
        self.OffSprings = list()
        for i in range(0,len(self.Parents)-1, 2):
            parent1 = self.Parents[i].copy()
            parent2 = self.Parents[i + 1].copy()
            offspring = [-1 for _ in range(len(parent1))]
            idx = random.randint(0,len(parent1)//2)
            offspring[idx: idx + len(parent1)//2] = parent1[idx:idx + len(parent1)//2]
            count_op = [0 for _ in range(self.J)]
            for x in offspring:
                if x != -1:
                    count_op[x] += 1
            c = 0
            for j in range( len(parent2)):
                if c == idx:
                    c = idx + len(parent2)//2
                if count_op[parent2[j]] < self.M:
                    offspring[c] = parent2[j]
                    c += 1
                    count_op[parent2[j]] += 1
            self.OffSprings.append(offspring)
            
    
    def Mutation(self):
        p = random.uniform(0,1)
        if p <= self.mutation_rate:
            for i in range(self.offspring_size):
                rnd1 = random.randint(0,len(self.OffSprings[i]) - 1)
                rnd2 = random.randint(0,len(self.OffSprings[i]) - 1)
                while rnd2 == rnd1:
                    rnd2 = random.randint(0,len(self.OffSprings[i]) - 1)
                if rnd1 < rnd2:
                    self.OffSprings[i] = self.OffSprings[i][:rnd1+1] + [self.OffSprings[i][rnd2]] + self.OffSprings[i][rnd1+1:rnd2] + self.OffSprings[i][rnd2+1:]
                else:
                    self.OffSprings[i] = self.OffSprings[i][:rnd2+1] + [self.OffSprings[i][rnd1]] + self.OffSprings[i][rnd2+1:rnd1] + self.OffSprings[i][rnd1+1:]
    
        












# def crossover(parents):
#     offsprings = []
#     for i in range(0, len(parents), 2):
#         parent1 = parents[i]
#         parent2 = parents[i+1]
#         child = {}
#         machines1 = [random.randint(0,self.M-1) for j in range(self.M//2)]
#         for j in machines1:
#             child[j] = parent1[j].copy()
#         for j in parent2:
#             if not(j in child):
#                 child[j] = parent2[j].copy()
#         offsprings.append(child)

#     print(offsprings[0])
#     return offsprings

# # offsprings = crossover(population)

# #print(selection(fitness_value, fitness_value, 'Truncation', 20, 5))

# # import plotly.express as px
# # import pandas as pd


# # df = pd.DataFrame([
# #     dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
# #     dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
# #     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')])

# # fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
# # fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
# # fig.show()
# # jobList = []
# # for i in offsprings[0].values():
# #     for j in i:
# #         if j[0] == 1:
# #             jobList.append(dict(Task = f"{j[0]},{j[1]}", Start = j[2], Finish = j[3], Resource = "S"))


# # import pandas as pd
# # import plotly.figure_factory as ff
# # ganttcharts = []
# # for i in range(len(offsprings)):
# #     ganttchart = []
# #     for j in offsprings[i][4]:
# #         ganttchart.append(dict(Task = f"{j[0]},{j[1]}", Start = j[2], Finish = j[3], Resource = "S"))
# #     ganttcharts.append(ganttchart)

# # df = pd.DataFrame(
# #     jobList
# # )

# # fig = ff.create_gantt(df, index_col = 'Resource',  bar_width = 0.4, show_colorbar=True)
# # fig.update_layout(xaxis_type='linear', autosize=False, width=800, height=400)
# # fig.show()

HyperParameters = {
    'Population Size': 30,
    'Generations': 5000,
    'Iterations': 10,
    'Mutation Rate': 1,
    'OffSpring Size': 10,
    'Parent Procedure': 'Random',
    'Survival Procedure': 'Random',
    'Tournament Size': 25,
    'Data Path': "abz7.txt"
}


JSSP1 = JSSP(HyperParameters)
JSSP1.Simulate()