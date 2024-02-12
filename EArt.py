import numpy as np
from tkinter import *
import random
import pygame
import pygame.gfxdraw
from copy import deepcopy
from time import perf_counter
from EA import *

class EArt(EA):
    def __init__(self, hyp):
        super().__init__(hyp)
        self.points = hyp['Points']
        self.PolygonSize = hyp['Polygon Size']
        self.screen = pygame.display.set_mode((10,10))
        self.image = pygame.image.load(self.datapath).convert()
        size = self.image.get_size()
        self.N = size[0]
        self.M = size[1]
        self.screen = pygame.display.set_mode((self.N, self.M))
        self.images = list()


    def initialize(self):
        for _ in range(self.population_size):
            polygons = list()
            for i in range(self.PolygonSize):
                polygon = dict()
                polygon['c'] = pygame.Color(random.randint(20,255), random.randint(20,255), random.randint(20,255), random.randint(20,255))
                polygon['v'] = [(random.randint(0,self.N-1), random.randint(0,self.M-1)) for _ in range(self.points)]
                polygons.append(polygon)
            self.Population.append(polygons)
            self.compute_max_diff()

    def compute_max_diff(self):
        d = 0
        for i in range(self.N):
            for j in range(self.M):
                rgba =  self.image.get_at((i,j))
                d += rgba[0] - 0
                d += rgba[1] - 0
                d += rgba[2] - 0
        self.maxdiff = d
    def fitness(self, idx):
        d = 0
        for i in range(self.N):
            for j in range(self.M):
                rgba1 =  self.image.get_at((i,j))
                rgba2 =  self.images[-1].get_at((i,j))
                d += abs(rgba1[0] - rgba2[0])
                d += abs(rgba1[1] - rgba2[1])
                d += abs(rgba1[2] - rgba2[2])
        
        return (d/self.maxdiff)*100

    def convert_to_image(self,idx, Pop):
        current_image = pygame.Surface((self.N, self.M), pygame.SRCALPHA)
        for i in Pop[idx]:
            pygame.gfxdraw.filled_polygon(current_image, i['v'], i['c'])
        return current_image
    
    def CrossOver(self):
        self.OffSprings = list()
        for i in range(0,len(self.Parents),2):
            parent1 = self.Parents[random.randint(0,len(self.Parents)-1)]
            parent2 = self.Parents[random.randint(0,len(self.Parents)-1)]
            offspring = []
            indices = [j for j in range(self.PolygonSize)]
            np.random.shuffle(indices)
            c = 0
            for z in range(self.PolygonSize):
                offspring.append(deepcopy(parent1[c]))
                c += 1
            for z in range(0):
                offspring.append(deepcopy(parent2[c]))
                c += 1
            self.OffSprings.append(offspring)
    
    def Mutation(self):
        for o in self.OffSprings:
            rnd1 = random.randint(1,300)
            rnd2 = random.randint(1,100)
            polygon_idx = random.randint(0,self.PolygonSize-1)
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
                        red_val = (color.r + random.randint(1,3))
                        if red_val > 255:
                            red_val = 255
                        o[polygon_idx]['c'] = pygame.Color(red_val, color.g, color.b, color.a)
                    else:
                        color = o[polygon_idx]['c']
                        o[polygon_idx]['c'] = pygame.Color(random.randint(0,255), color.g, color.b, color.a)
                elif rnd1 <= 75:
                    if rnd2 <= 50:
                        color = o[polygon_idx]['c']
                        green_val = (color.g + random.randint(1,3))
                        if green_val > 255:
                            green_val = 255
                        o[polygon_idx]['c'] = pygame.Color(color.r, green_val, color.b, color.a)
                    else:
                        color = o[polygon_idx]['c']
                        o[polygon_idx]['c'] = pygame.Color(color.r, random.randint(0,255), color.b, color.a)
                elif rnd1 <= 100:
                    if rnd2 <= 50:
                        color = o[polygon_idx]['c']
                        blue_val = (color.b + random.randint(1,3))
                        if blue_val > 255:
                            blue_val = 255
                        o[polygon_idx]['c'] = pygame.Color(color.r, color.g, blue_val, color.a)
                    else:
                        color = o[polygon_idx]['c']
                        o[polygon_idx]['c'] = pygame.Color(color.r, color.g, random.randint(0,255), color.a)
            elif rnd1 <= 200:
                point_idx = random.randint(0,self.points-1)
                if rnd1 <= 150:
                    if rnd2 <= 50:
                        vert = o[polygon_idx]['v'][point_idx]
                        o[polygon_idx]['v'][point_idx] = ((vert[0] + random.randint(1,self.N//10))%self.N, vert[1])
                    else:
                        vert = o[polygon_idx]['v'][point_idx]
                        o[polygon_idx]['v'][point_idx] = (random.randint(0,self.N-1), vert[1])
                else:
                    if rnd2 <= 50:
                        vert = o[polygon_idx]['v'][point_idx]
                        o[polygon_idx]['v'][point_idx] = (vert[0], (vert[1] + random.randint(1,self.M//10))%self.M)
                    else:
                        vert = o[polygon_idx]['v'][point_idx]
                        o[polygon_idx]['v'][point_idx] = (vert[0], random.randint(0,self.M-1))
            else:
                o[polygon_idx]['v'] = [(random.randint(0,self.N-1), random.randint(0,self.M-1)) for _ in range(self.points)]

    def EvaluateFitness(self, r):
        self.images = list()
        if r == 'P':
            for i in range(len(self.Population)):
                self.images.append(self.convert_to_image(i, self.Population))
                self.fit_lst.append(self.fitness(i))
        elif r == 'O':
            for i in range(len(self.OffSprings)):
                self.images.append(self.convert_to_image(i, self.OffSprings))
                self.fit_lst.append(self.fitness(i))
    def DisplayGenerationInfo(self):
        super().DisplayGenerationInfo()
        out = self.convert_to_image(0, self.Population)
        if self.current_generation % 500 == 0:
            pygame.image.save(out, f"ml_{self.current_iteration}_{self.current_generation}.jpg")

