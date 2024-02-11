import numpy as np
from tkinter import *
import random
import pygame
import pygame.gfxdraw
from copy import deepcopy
from time import perf_counter

def initialize(pop_size, pol_size, N, M):
    population = list()
    for _ in range(pop_size):
        polygons = list()
        for i in range(pol_size):
            polygon = dict()
            polygon['c'] = pygame.Color(random.randint(20,255), random.randint(20,255), random.randint(20,255), random.randint(20,255))
            polygon['v'] = [(random.randint(0,N-1), random.randint(0,M-1)) for _ in range(points)]
            polygons.append(polygon)
        population.append(polygons)
    return population

def compute_max_diff(image, N, M):
    d = 0
    for i in range(N):
        for j in range(M):
            rgba =  image.get_at((i,j))
            d += 255 - rgba[0]
            d += 255 - rgba[1]
            d += 255 - rgba[2]
            # image.set_at((i,j),pygame.Color(rgba[0], 0, 0, 255))
    return d

def compute_diff(image1, image2, N, M):
    d = 0
    for i in range(N):
        for j in range(M):
            rgba1 =  image1.get_at((i,j))
            rgba2 =  image2.get_at((i,j))
            d += abs(rgba1[0] - rgba2[0])
            d += abs(rgba1[1] - rgba2[1])
            d += abs(rgba1[2] - rgba2[2])
    return d

def convert_to_image(polygons, N,M):
    current_image = pygame.Surface((N, M), pygame.SRCALPHA)
    current_image.fill(pygame.Color("white"))
    for i in polygons:
        pygame.gfxdraw.filled_polygon(current_image, i['v'], i['c'])
    return current_image

def selection_procedure(Population, images, fitness_val, procedure, selected_size):
    if procedure == 'Truncation':
        idx_lst = list(reversed(np.argsort(fitness_val)))
        return ([Population[idx_lst[i]] for i in range(selected_size)], [images[idx_lst[i]] for i in range(selected_size)], [fitness_val[idx_lst[i]] for i in range(selected_size)])

def crossover(parents):
    offsprings = []
    for i in range(0,len(parents),2):
        parent1 = parents[random.randint(0,len(parents)-1)]
        parent2 = parents[random.randint(0,len(parents)-1)]
        offspring = []
        indices = [j for j in range(polygon_size)]
        np.random.shuffle(indices)
        c = 0
        for z in range(polygon_size):
            offspring.append(deepcopy(parent1[c]))
            c += 1
        for z in range(0):
            offspring.append(deepcopy(parent2[c]))
            c += 1
        offsprings.append(offspring)
    return offsprings

def mutation(offsprings):
    for o in offsprings:
        rnd1 = random.randint(1,280)
        rnd2 = random.randint(1,100)
        polygon_idx = random.randint(0,polygon_size-1)
        if (rnd1 <= 100):
            if o[polygon_idx]['c'].a < 0.01 or rnd1 <= 25:
                if rnd2 <= 50:
                    color = o[polygon_idx]['c']
                    o[polygon_idx]['c'] = pygame.Color(color.r, color.g, color.b, (color.a + random.randint(1,3))%255)
                else:
                    color = o[polygon_idx]['c']
                    o[polygon_idx]['c'] = pygame.Color(color.r, color.g, color.b, random.randint(10,255))
            elif rnd1 <= 50:
                if rnd2 <= 50:
                    color = o[polygon_idx]['c']
                    red_val = (color.r + random.randint(1,3))%255
                    if red_val > 255:
                        red_val = 255
                    o[polygon_idx]['c'] = pygame.Color(red_val, color.g, color.b, color.a)
                else:
                    color = o[polygon_idx]['c']
                    o[polygon_idx]['c'] = pygame.Color(random.randint(0,255), color.g, color.b, color.a)
            elif rnd1 <= 75:
                if rnd2 <= 50:
                    color = o[polygon_idx]['c']
                    green_val = (color.r + random.randint(1,3))%255
                    if green_val > 255:
                        green_val = 255
                    o[polygon_idx]['c'] = pygame.Color(color.r, green_val, color.b, color.a)
                else:
                    color = o[polygon_idx]['c']
                    o[polygon_idx]['c'] = pygame.Color(color.r, random.randint(0,255), color.b, color.a)
            elif rnd1 <= 100:
                if rnd2 <= 50:
                    color = o[polygon_idx]['c']
                    blue_val = (color.r + random.randint(1,3))%255
                    if blue_val > 255:
                        blue_val = 255
                    o[polygon_idx]['c'] = pygame.Color(color.r, color.g, blue_val, color.a)
                else:
                    color = o[polygon_idx]['c']
                    o[polygon_idx]['c'] = pygame.Color(color.r, color.g, random.randint(0,255), color.a)
        elif rnd1 <= 200:
            point_idx = random.randint(0,points-1)
            if rnd1 <= 150:
                if rnd2 <= 50:
                    vert = o[polygon_idx]['v'][point_idx]
                    o[polygon_idx]['v'][point_idx] = ((vert[0] + random.randint(1,N//10))%N, vert[1])
                else:
                    vert = o[polygon_idx]['v'][point_idx]
                    o[polygon_idx]['v'][point_idx] = (random.randint(0,N-1), vert[1])
            else:
                if rnd2 <= 50:
                    vert = o[polygon_idx]['v'][point_idx]
                    o[polygon_idx]['v'][point_idx] = (vert[0], (vert[1] + random.randint(1,M//10))%M)
                else:
                    vert = o[polygon_idx]['v'][point_idx]
                    o[polygon_idx]['v'][point_idx] = (vert[0], random.randint(0,M-1))
        else:
            o[polygon_idx]['v'] = [(random.randint(0,N-1), random.randint(0,M-1)) for _ in range(points)]
        
    
        
            
            
            
    


N = 200
M = 200

screen = pygame.display.set_mode((N*2,M))
image = pygame.image.load("mona_lisa_v2.png").convert()


points = 6
population_size = 1
polygon_size = 50
offspring_size = 1
iterations = 100001
iter = 0

Population = initialize(population_size, polygon_size, N, M)
max_diff = compute_max_diff(image, N, M)
screen.blit(image, (0,0))
pygame.display.flip()
# Computing Fitness
fitness_val = list()
images = list()
for i in range(population_size):
    images.append(convert_to_image(Population[i], N, M))
for i in range(population_size):
    diff = compute_diff(image, images[i], N, M)
    fitness = (1 - diff / max_diff)*100
    # fitness = diff
    fitness_val.append(fitness)

while iter < iterations:
    if iter%100 == 0:
        print("Iteration No.", iter, min(fitness_val))
        pygame.image.save(screen, "mona-lisa.jpg")


    

    # converting polygons to images = 
    # time1 = perf_counter()
    
    # time2 = perf_counter()
    # print("Time Taken 1:", time2 - time1)

    # time1 = perf_counter()

    # time2 = perf_counter()
    # print("Time Taken 2:", time2 - time1)

    # print("Fitness Value:", list(sorted(fitness_val)), end='\n\n')

    # Selection
    # parents = selection_procedure(Population, images, fitness_val, 'Truncation', offspring_size)
    parents = [Population[0].copy() for _ in range(offspring_size)]
    screen.fill(pygame.Color("black"))
    screen.blit(image, (0,0))
    screen.blit(images[0], (N,0))
    # print("Min Fitness Value", min(fitness_val), end='\n\n')

    # crossover
    # offsprings = crossover(parents[0])

    # mutation
    offsprings = [deepcopy(i) for i in parents]
    mutation(offsprings)

    image_offsprings = list()
    for j in offsprings:
        image_offsprings.append(convert_to_image(j, N, M))
    
    


    Total_Pop = Population + offsprings
    Total_img = images + image_offsprings

    for i in range(offspring_size):
        diff = compute_diff(image, image_offsprings[i], N, M)
        fitness = (1 - diff / max_diff)*100
        # fitness = diff 
        fitness_val.append(fitness)
    # print("Fitness Value:", list(sorted(fitness_val)), end='\n\n')
    # print(list(sorted(fitness_val)))

    Population = selection_procedure(Total_Pop, Total_img, fitness_val, 'Truncation', population_size)
    images = Population[1]
    fitness_val = Population[2]
    Population = Population[0]
    
    
    pygame.display.flip()
    iter += 1

# print(Population[0])




# screen.blit(current_image, (N,0))


status = True
while (status):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False

pygame.quit()