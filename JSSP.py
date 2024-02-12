from EA import *

class JSSP(EA):
    def __init__(self, hyp) -> None:
        super().__init__(hyp)
        self.Jobs = dict()
        with open("CI-HW1/abz5.txt", "r") as file:
            lst = [[int(j) for j in i.strip().split()] for i in file]
            self.J = lst[0][0]
            self.M = lst[0][1]
            for i in range(1,len(lst)):
                self.Jobs[i-1] = list()
                for j in range(0,len(lst[i]),2):
                    self.Jobs[i-1].append((lst[i][j], lst[i][j+1]))

    def initialize(self) -> None:
        self.Population = list()
        for i in range(self.population_size):
            current_operation = [0 for _ in range(self.J)] 
            current_time = [0 for _ in range(self.M)]
            prev_operation_end_time = [0 for _ in range(self.J)]
            MOT = {i:list() for i in range(self.M)} 
            finished_jobs = 0
            while finished_jobs != self.J:
                current_job = random.randint(0, self.J-1) # Picking a random job
                while current_operation[current_job] == self.M: # Check to not schedule already finished jobs
                    current_job = random.randint(0, self.J-1)
                operation = current_operation[current_job]
                machine = self.Jobs[current_job][operation][0]
                req_time = self.Jobs[current_job][operation][1]
                if current_time[machine] < prev_operation_end_time[current_job]: # Check for previous operation completion
                    start_time = prev_operation_end_time[current_job]
                else:
                    start_time = current_time[machine]
                end_time = start_time + req_time
                prev_operation_end_time[current_job] = end_time
                current_time[machine] = end_time
                current_operation[current_job] += 1
                if current_operation[current_job] == self.M: # Check for marking a job as finished
                    finished_jobs += 1
                MOT[machine].append((current_job, operation, start_time, end_time))
            self.Population.append(MOT)
    
    def fitness(self, p):
        return max([i[-1][-1] for i in p.values()])
    
    def is_consistent(self, p):
        operation_consistent = True
        machine_consistent = True
        op_time = [[None for _ in range(self.M)] for _ in range(self.J)]
        for i in p:
            time = 0
            for j in p[i]:
                op_time[j[0]][j[1]] = (j[2], j[3])
                if j[2] < time and j[1] != 0:
                    print(j)
                    machine_consistent = False
                    time = j[3]
                    break
                else:
                    time = j[3]
        if not(machine_consistent):
            return machine_consistent
        for i in op_time:
            for j in range(len(i)-1):
                if i[j][1] > i[j+1][1]:
                    print(j)
                    operation_consistent = False
                    break
        return operation_consistent 
        

    def CrossOver(self, parents):
        self.OffSprings = list()
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i+1]
            child = dict()
            machines1 = [random.randint(0,self.M-1) for j in range(self.M//2)]
            for j in machines1:
                child[j] = parent1[j].copy()
            for j in parent2:
                if not(j in child):
                    child[j] = parent2[j].copy()
            prev_operation_time = [0 for _ in range(self.M)]
            machine_times = [0 for _ in range(self.M)]
            for x in range(self.M):
                for y in range(self.J):
                    machine_no = self.Jobs[y][x][0]
                    duration = self.Jobs[y][x][1]
                    for k in range(len(child[machine_no])):
                        opp = child[machine_no][k]
                        if opp[0] == y and opp[1] == x:
                            print("Before", opp)
                            start_time = max(machine_times[machine_no], prev_operation_time[y])
                            end_time = start_time + duration
                            child[machine_no][k] = (opp[0], opp[1], start_time, end_time)
                            prev_operation_time[y] = end_time
                            machine_times[machine_no]= end_time
                            print(machine_times)
                            print(prev_operation_time)
                            print("After", child[machine_no][k])
                            break
            print(child)
            print(self.is_consistent(child))
            int("shdsd")
            self.OffSprings.append(child)
        for i in self.OffSprings:
            print(self.is_consistent(i))
        print(self.OffSprings[0])
    
    def Mutation(self):
        pass
    
        












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