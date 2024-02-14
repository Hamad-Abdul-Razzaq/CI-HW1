# Importing the matplotlib.pyplot
import matplotlib.pyplot as plt
Jobs = dict()
with open("abz5.txt", "r") as file:
    lst = [[int(j) for j in i.strip().split()] for i in file]
    J = lst[0][0]
    M = lst[0][1]
    for i in range(1,len(lst)):
        Jobs[i-1] = list()
        for j in range(0,len(lst[i]),2):
            Jobs[i-1].append((lst[i][j], lst[i][j+1]))
# print(Jobs)

def fitness(p, J, M, Jobs):
    MOT = {i : list() for i in range(M)}
    current_operation = [0 for _ in range(J)]
    prev_operation_time = [0 for _ in range(J)]
    machine_time = [0 for _ in range(M)]
    for j in p:
        o = current_operation[j]
        m = Jobs[j][o][0]
        duration = Jobs[j][o][1]
        st = max(machine_time[m], prev_operation_time[j])
        sp = st + duration
        machine_time[m] =  sp
        prev_operation_time[j] = machine_time[m]
        MOT[m].append((st,duration))
        current_operation[j] += 1
    return(MOT)

p = [1, 2, 5, 8, 9, 4, 7, 7, 5, 2, 1, 7, 6, 0, 8, 6, 7, 0, 3, 8, 5, 6, 8, 5, 4, 9, 2, 1, 0, 6, 5, 3, 9, 2, 1, 5, 7, 7, 0, 8, 3, 8, 9, 1, 4, 9, 9, 2, 3, 9, 8, 4, 0, 3, 6, 5, 2, 7, 3, 6, 0, 8, 5, 9, 1, 3, 2, 5, 0, 4, 8, 7, 2, 6, 1, 4, 3, 7, 2, 8, 0, 6, 5, 3, 9, 2, 7, 0, 3, 9, 1, 4, 6, 4, 0, 6, 1, 4, 1, 4]
MOT = fitness(p, J, M, Jobs)

# Declaring a figure "gnt"
fig, gnt = plt.subplots()

# Setting Y-axis limits
gnt.set_ylim(0, 50)

# Setting X-axis limits
gnt.set_xlim(0, 160)

# Setting labels for x-axis and y-axis
gnt.set_xlabel('Time')
gnt.set_ylabel('Machine')

# Setting ticks on y-axis
gnt.set_yticks([15, 25, 35, 45])
# Labelling tickes of y-axis
gnt.set_yticklabels(['1', '2', '3', '4'])

# Setting graph attribute
# gnt.grid(True)


# Declaring a bar in schedule
gnt.broken_barh([(0, 94), (94, 153), (153, 236), (461, 556), (630, 729), (729, 791), (793, 885), (885, 961), (961, 1049), (1049, 1135)], (30, 9), facecolors =('tab:orange'))

# Declaring multiple bars in at same level and same width
gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
						facecolors ='tab:blue')

gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
								facecolors =('tab:red'))

plt.savefig("gantt1.png")
