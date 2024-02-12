import random
import numpy as np
Jobs = dict()
with open("CI-HW1/abz5.txt", "r") as file:
    lst = [[int(j) for j in i.strip().split()] for i in file]
    J = lst[0][0]
    M = lst[0][1]

    for i in range(1,len(lst)):
        Jobs[i-1] = list()
        for j in range(0,len(lst[i]),2):
            Jobs[i-1].append((lst[i][j], lst[i][j+1]))

        
# print(Jobs)
population_size = 30
population = []
maxtimes = []
for i in range(population_size):
    current_operation = [0 for _ in range(J)]  # [0 0 0 0 0 0 ..... 0]
    '''
    Value = Current Operation Number
    Index = Job No.
    '''
    current_time = [0 for _ in range(M)]
    '''
    Value = Elapsed Time on Machine
    Index = Machine no.
    '''
    prev_operation_end_time = [0 for _ in range(J)]

    MOT = dict() # Key: Machine number
    for i in range(M):
        MOT[i] = list()
    # print("MOT", MOT)
    finished_jobs = 0
    iteration = 0

    while finished_jobs != J:
        current_job = random.randint(0, J-1) # Picking a random job
        while current_operation[current_job] == M: # Check to not schedule already finished jobs
            current_job = random.randint(0, J-1)

        operation = current_operation[current_job]
        machine = Jobs[current_job][operation][0]
        req_time = Jobs[current_job][operation][1]

        if current_time[machine] < prev_operation_end_time[current_job]: # Check for previous operation completion
            start_time = prev_operation_end_time[current_job]
        else:
            start_time = current_time[machine]
        end_time = start_time + req_time
        prev_operation_end_time[current_job] = end_time
        current_time[machine] = end_time
        current_operation[current_job] += 1
        if current_operation[current_job] == M: # Check for marking a job as finished
            finished_jobs += 1
        #print("Current Time", current_time)
        #print("Current Operation", current_operation)
        MOT[machine].append((current_job, operation, start_time, end_time))
        #print("Chromosome", MOT)
        iteration += 1
    population.append(MOT)
    maxtimes.append(max(current_time))
    print(MOT)

fitness_value = maxtimes
print(fitness_value)

def selection(fitness_value, population, procedure, selectSize, tournament_size):
    if procedure == 'Truncation':
        idx_lst = np.argsort(fitness_value)
        print(type(fitness_value))
        print(type(population))
        return [population[idx_lst[i]] for i in range(selectSize)]
    elif procedure == 'TS':
        Tsample_idx = [random.randint(0,len(population)-1) for i in range(tournament_size)]
        Tsample = [population[Tsample_idx[i]] for i in range(len(Tsample_idx))]
        fitness_vals = [fitness_value[Tsample_idx[i]] for i in range(len(Tsample_idx))]
        idx_lst = np.argsort(fitness_vals)
        return(Tsample[idx_lst[i]] for i in range(len(Tsample_idx)))
    elif procedure == 'Rank Selection':
        idx_lst = np.argsort(fitness_value)
        descending_population = [population[idx_lst[i]] for i in range(len(idx_lst)-1,-1,-1)]
        rangeDict = {i: ((i*(i-1)/2*3000/len(population)), ((i)*(i+1)/2*3000/len(population))) for i in range(1,len(population) + 1)}
        selected = []
        minVal = 0
        maxVal = (len(population)*(len(population)+1)/2*3000)/len(population)
        selectedVals = [random.randint(minVal, maxVal) for i in range(selectSize)]
        for i in range(len(selectedVals)):
            for j in rangeDict:
                if rangeDict[j][0] <= selectedVals[i] < rangeDict[j][1]:
                    selected.append(descending_population[j-1])
        return selected

def crossover(parents):
    offsprings = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i+1]
        child = {}
        machines1 = [random.randint(0,M-1) for j in range(M//2)]
        for j in machines1:
            child[j] = parent1[j].copy()
        for j in parent2:
            if not(j in child):
                child[j] = parent2[j].copy()
        offsprings.append(child)

    print(offsprings[0])
    return offsprings

# offsprings = crossover(population)

#print(selection(fitness_value, fitness_value, 'Truncation', 20, 5))

# import plotly.express as px
# import pandas as pd


# df = pd.DataFrame([
#     dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
#     dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
#     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')])

# fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
# fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
# fig.show()
# jobList = []
# for i in offsprings[0].values():
#     for j in i:
#         if j[0] == 1:
#             jobList.append(dict(Task = f"{j[0]},{j[1]}", Start = j[2], Finish = j[3], Resource = "S"))


# import pandas as pd
# import plotly.figure_factory as ff
# ganttcharts = []
# for i in range(len(offsprings)):
#     ganttchart = []
#     for j in offsprings[i][4]:
#         ganttchart.append(dict(Task = f"{j[0]},{j[1]}", Start = j[2], Finish = j[3], Resource = "S"))
#     ganttcharts.append(ganttchart)

# df = pd.DataFrame(
#     jobList
# )

# fig = ff.create_gantt(df, index_col = 'Resource',  bar_width = 0.4, show_colorbar=True)
# fig.update_layout(xaxis_type='linear', autosize=False, width=800, height=400)
# fig.show()