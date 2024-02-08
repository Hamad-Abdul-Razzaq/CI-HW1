import random
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
    print("Current Time", current_time)
    print("Current Operation", current_operation)
    MOT[machine].append((current_job, operation, start_time, end_time))
    print("Chromosome", MOT)
    iteration += 1

#     print(MOT)
#     break