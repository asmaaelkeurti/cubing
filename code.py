        xk=np.arange(math.ceil(sum(list(map(lambda box:box.volume, self.boxes)))/self.pallets[0].volume),len(self.boxes))
        pk = np.histogram(stats.gamma.rvs(0.8,scale=1,size=10000000), bins=len(xk))[0]/10000000
        return 100-stats.percentileofscore(stats.rv_discrete(values=(xk,pk)).rvs(size=50000),len(self.pallets),kind='mean')