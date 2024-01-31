lst = []
with open("qa194.tsp","r") as file:
    lst = [i.strip().split() for i in file]
for _ in range(7):
    lst.pop(0)
lst.pop(-1)
lst = [[float(i) for i in j] for j in lst]
distance = [[0 for _ in range(len(lst))] for __ in range(len(lst))]
for i in range(len(lst)):
    for j in range(i+1,len(lst)):
        distance[i][j] = distance[j][i] = ((lst[i][1] - lst[j][1])**2 + (lst[i][2] - lst[j][2])**2)**(1/2)
with open ("distance.txt", "w") as file:
    for i in range(len(distance)):
        for j in range(len(distance)):
            file.write(f"{distance[i][j]} ")
        file.write("\n")