import random
Jobs = dict()
with open("abz5.txt", "r") as file:
    lst = [[int(j) for j in i.strip().split()] for i in file]
    J = lst[0][0]
    M = lst[0][1]

    for i in range(1,len(lst)):
        Jobs[i-1] = list()
        current_time = 0
        for j in range(0,len(lst[i]),2):
            Jobs[i-1].append((lst[i][j], current_time, current_time +  lst[i][j+1]))
            current_time +=  lst[i][j+1]

        
print(Jobs)
current_operation = [0 for _ in range(J)]
current_time = [0 for _ in range(M)]
MOT = dict()
for i in range(M):
    MOT[i] = list()

finised = False
while not(finised):
    job = random.randint(0, J-1)
    operation = current_operation[job]
    machine = Jobs[job][current_operation[job]][0]
    req_time = Jobs[job][current_operation[job]][1]
    MOT[machine].append((job, operation, current_time[machine], current_time[machine] + ))

    print(MOT)
    break