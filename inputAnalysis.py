# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 21:50:43 2017

@author: liweijun
"""
import json
import numpy as np
import scipy.stats as stats
from pandas.io.json import json_normalize
import seaborn as sns
import math
import matplotlib.pyplot as plt

class pallet(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.boxes = []
        self.volume = x*y*z
        
    def center_of_mass(self):
        a = np.array(list(map(lambda x:np.array([x.startPoint['x'] + x.bestOption['x']/2.0,x.startPoint['y'] + x.bestOption['y']/2.0,x.startPoint['z'] + x.bestOption['z']/2.0,x.weight]),self.boxes)))
        return list(np.average(a[:,:3],axis=0,weights=a[:,3]))
    
    def std(self):
        return np.sqrt((self.center_of_mass()[0] - self.x/2)**2 + (self.center_of_mass()[1] - self.y/2)**2)
    
    def adjusted_std(self):
        return self.std()/np.sqrt(np.average(list(map(lambda box:box.x,self.boxes)))**2 + np.average(list(map(lambda box:box.y,self.boxes)))**2)
        
class box(object):
    def __init__(self,x,y,z,weight,startPoint,bestOption):
        self.x = x
        self.y = y
        self.z = z
        self.weight = weight
        self.startPoint = startPoint
        self.bestOption = bestOption
        self.volume = x*y*z



class cubingResult(object):
    def __init__(self):
        self.data = json.loads(open('C:\\Users\\liweijun\\Desktop\\新建文件夹\\Elkeurti\\cubingData.json').read())   
        self.pallets = []
        self.boxes = []
        
        for loadUnit in self.data['loadUnits']:
            p = pallet(loadUnit['x'],loadUnit['y'],loadUnit['z'])
            for b in loadUnit['PlacedBoxes']:
                p.boxes.append(box(b['x'],b['y'],b['z'],b['weight'],b['startPoint'],b['bestOption']))
                self.boxes.append(box(b['x'],b['y'],b['z'],b['weight'],b['startPoint'],b['bestOption']))
            self.pallets.append(p)
            
    def display_data(self):
        a = json_normalize(self.data['Boxes'])
        aa = a[['x','y','z']]
        sns.set()
        sns.pairplot(aa,size=3)
    
    def display_pallets_number_distribution(self):
        plt.hist(stats.gamma.rvs(2.5,scale=1,size=1000000), bins=100)
    
    def average_center_of_mass_height(self):
        return np.average(list(map(lambda x:x.center_of_mass()[2],self.pallets)))
    
    def pallets_center_of_mass_variance(self):
        return np.sum(list(map(lambda p:(p.center_of_mass()[0] - p.x)**2 + (p.center_of_mass()[1] - p.y)**2,self.pallets)))/len(self.pallets)

    def pallets_number_evaluation(self):
        xk=np.arange(math.ceil(sum(list(map(lambda box:box.volume, self.boxes)))/self.pallets[0].volume),len(self.boxes))
        pk = np.histogram(stats.gamma.rvs(0.8,scale=1,size=10000000), bins=len(xk))[0]/10000000
        return 100-stats.percentileofscore(stats.rv_discrete(values=(xk,pk)).rvs(size=50000),len(self.pallets),kind='mean')
    
    def center_of_mass_horizontal_evaluation(self):
        xk = np.arange(0,np.sqrt(self.pallets[0].x**2 + self.pallets[0].y**2)*len(self.pallets))
        pk = np.histogram(stats.gamma.rvs(2.5,scale=1,size=10000000), bins=len(xk))[0]/10000000
        return 100-stats.percentileofscore(stats.rv_discrete(values=(xk,pk)).rvs(size=50000),sum(list(map(lambda pallet:pallet.std(),self.pallets))),kind='mean')
    
    def center_of_mass_vertical_evaluation(self):
        xk = np.arange(0,self.pallets[0].y)
        pk = np.histogram(stats.gamma.rvs(100,scale=2,size=10000000), bins=len(xk))[0]/10000000
        return 100-stats.percentileofscore(stats.rv_discrete(values=(xk,pk)).rvs(size=50000),np.average(list(map(lambda pallet:pallet.center_of_mass()[2],self.pallets))),kind='mean')

                     
                         
c = cubingResult()
print(c.center_of_mass_vertical_evaluation()*0.3 + c.pallets_number_evaluation()*0.4 + c.center_of_mass_horizontal_evaluation()*0.3)
c.display_pallets_number_distribution()
##print(c.center_of_mass_horizontal_evaluation())

#xk = np.arange(4,200)
#pk = np.histogram(stats.gamma.rvs(1.5,scale=1,size=10000000), bins=len(xk))[0]/10000000
#print(100-stats.percentileofscore(stats.rv_discrete(values=(xk,pk)).rvs(size=50000),8,kind='mean'))

