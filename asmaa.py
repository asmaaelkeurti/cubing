# -*- coding: utf-8 -*-
"""
Created on Tue May 16 23:02:27 2017

@author: liweijun
"""
import random
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import uuid

class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

class UnitCube:
    def __init__(self, x,y,z):
        self.location = [x,y,z]
        self.status = True

class Box:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.vol = x*y*z
        
        self.option = [
			[x,y,z],
			[x,z,y],
			[y,x,z],
			[y,z,x],
			[z,x,y],
			[z,y,x]
                ]

class Container:
    def __init__(self,width,length,height):
        self.width = width
        self.length = length
        self.height = height
        self.container = []
        
        for i in range(0,width):
            for j in range(0,length):
                for k in range(0,height):
                    self.container.append(UnitCube(i,j,k))
        
    def place_boxs(self,boxs,genes):  
        for c in self.container:
            c.status = True
                      
        for i in range(0,len(boxs)):
            for unitcube in self.find_all_available_cubes():
                if self.check_occupySpace(boxs[i].option[genes[i]], unitcube):
                    self.update_space(boxs[i].option[genes[i]], unitcube)
                    break
        
    def find_all_available_cubes(self):
        available_points = []
        
        for i in range(0,self.width):
            for j in range(0,self.length):
                for k in range(0,self.height):
                    cube = self.find_unitCube(i,j,k)
                    if cube.status == True:
                        available_points.append(cube)
                        break
        
        return available_points
    
    def check_occupySpace(self,option,startCube):
        for i in range(startCube.location[0], startCube.location[0] + option[0]):
            for j in range(startCube.location[1], startCube.location[1] + option[1]):
                for k in range(startCube.location[2], startCube.location[2] + option[2]):
                    if not self.find_unitCube(i,j,k).status :return False
        return True
    
    
    def update_space(self,option,startCube):
        for i in range(startCube.location[0], startCube.location[0] + option[0]):
            for j in range(startCube.location[1], startCube.location[1] + option[1]):
                for k in range(startCube.location[2], startCube.location[2] + option[2]):
                    self.find_unitCube(i,j,k).status = False
                      
    
        
    def find_unitCube(self,x,y,z):
        for unitCube in self.container:
            if unitCube.location == [x,y,z]:return unitCube
    
        unitCube = UnitCube(-1,-1,-1)
        unitCube.status = False
        return unitCube   
   

def _generate_parent(length, geneSet, get_fitness):    
    genes = []
    while len(genes) < length:
        genes.extend(random.sample(geneSet, 1))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)

def _mutate(parent, geneSet, get_fitness, startGeneIndex, endGeneIndex,numOfGene):
    childGenes = parent.Genes[:]
    for i in range(0,numOfGene):
        index = random.randrange(startGeneIndex, endGeneIndex+1)
        newGene, alternate = random.sample(geneSet, 2)
        childGenes[index] = alternate if newGene == childGenes[index] else newGene
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness)

def _get_boxs(boxsData):
    boxs = []
    for i in boxsData:
        boxs.append(Box(i[0],i[1],i[2]))
    boxs.sort(key = lambda x:x.vol)
    boxs.reverse()
    #container = Container(10,10,10)
    i = 0
    volSum = 0
    while(volSum < len(container.container)):
        volSum = volSum + boxs[i].vol
        i = i + 1
    boxs = boxs[:i]
    return boxs

def _basic_GA(boxsData, container):
    boxs = _get_boxs(boxsData)
    geneSet = [0,1,2,3,4,5]
    def get_fitness(genes):
        return _get_fitness(boxs,genes,container)
    def display(candidate):
        _display(candidate, startTime)
    
    random.seed()
    startTime = datetime.datetime.now() 
    bestParent = _generate_parent(len(boxs),geneSet,get_fitness)
    display(bestParent)
    new_data = []
    test_id = int(uuid.uuid1())
    reboot = 0
    mutationData = _Get_data()
    mutation_id = 0
    bestFitness = 0
    try:
        while True:
            child = _mutate(bestParent,geneSet, get_fitness, 0, len(boxs)-1, 1)
            display(child)
            x = random.randrange(0,1000)
            plt.scatter(x,child.Fitness)
            plt.pause(0.01)
            
            mutation_id = mutation_id + 1
            
            if bestParent.Fitness >= child.Fitness:
                    reboot = reboot + 1
                    if reboot >= (len(boxs))*3:
                        random.seed()
                        bestParent = _generate_parent(len(boxs),geneSet,get_fitness)
                        reboot = 0
                    continue
            bestParent = child
            reboot = 0
            
            if bestFitness < bestParent.Fitness:
                new_data.append((test_id, mutation_id, child.Fitness, datetime.datetime.now() - startTime))
                bestFitness = bestParent.Fitness
            
    except KeyboardInterrupt:
        print('Test Interrupted')
    mutationData = mutationData.append(pd.DataFrame(data=new_data, columns=mutationData.columns))
    _Commit(mutationData)

def _single_bin_packing(boxsData, container):
    boxs = _get_boxs(boxsData)
    geneSet = [0,1,2,3,4,5]

    def get_fitness(genes):
        return _get_fitness(boxs,genes,container)
    
    def display(candidate):
        _display(candidate, startTime)
    
    random.seed()
    startTime = datetime.datetime.now()
    bestParent = _generate_parent(len(boxs),geneSet,get_fitness)
    display(bestParent)
    
    mutateInterval = 5
    mutateTimes = 3
    
    startGeneIndex = 0
    endGeneIndex = mutateInterval-1
    
    mutationData = _Get_data()
    
    new_data = []
    test_id = int(uuid.uuid1())
    mutation_id = 0
    try:
        while True:
            for i in range(0,mutateInterval*mutateTimes):
                child = _mutate(bestParent, geneSet, get_fitness, startGeneIndex, endGeneIndex,mutateInterval - int(i/mutateTimes))
                
                
                display(child)
                x = random.randrange(0,1000)
                plt.scatter(x,child.Fitness)
                plt.pause(0.01)
            
                if bestParent.Fitness >= child.Fitness:
                    continue
                #display(child)
                bestParent = child
                new_data.append((test_id, mutation_id, child.Fitness, datetime.datetime.now() - startTime))
                
                mutation_id = mutation_id + 1
            
            
            startGeneIndex = endGeneIndex + 1
            endGeneIndex = startGeneIndex + 5
            
            if startGeneIndex >= len(bestParent.Genes):
                startGeneIndex = 0
                endGeneIndex = 4
                bestParent = _generate_parent(len(boxs),geneSet,get_fitness)
            elif endGeneIndex >= len(bestParent.Genes):
                endGeneIndex = len(bestParent.Genes)-1
    except KeyboardInterrupt:
        print('Test Interrupted') 
    mutationData = mutationData.append(pd.DataFrame(data=new_data, columns=mutationData.columns))
    _Commit(mutationData)


def _get_fitness(boxs, genes, container):
    container.place_boxs(boxs,genes)
    return sum(c.status == False for c in container.container)/(len(container.container))
    
def _display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}".format(
        ''.join(str(e) for e in candidate.Genes),
        candidate.Fitness,
        timeDiff))


def _create_boxsData(x,y,z,num):
    boxsData = []
    for i in range(0,num):
        boxsData.append([x,y,z])
    return boxsData
    
    
#container = Container(3,3,3)
#container.place_boxs([Box(2,2,2),Box(1,1,3)],[1,2])
#for b in container.container:
#    print(b.status)

def _Commit(data):
    data.to_pickle("C:\\Users\\liweijun\\Desktop\\新建文件夹\\python-GA\\Mutation.pkl")
    
def _Get_data():
    return pd.read_pickle("C:\\Users\\liweijun\\Desktop\\新建文件夹\\python-GA\\Mutation.pkl")

boxsData = [[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],
[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],
[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],
[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],
[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,3],[2,2,3],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],[2,2,3],[2,2,4],[2,3,4],
]


#a = _Get_data()
#a = a.iloc[0:0] 
#_Commit(a)


container = Container(1*4,2*4,3*4)
#_single_bin_packing(_create_boxsData(1,2,3,300), container)
_basic_GA(_create_boxsData(1,2,3,300), container)
    
    
