class World:
    def __init__(self, spp1, spp2, res1, res2):
        self.spp1 = spp1
        self.spp2 = spp2
        self.res1 = res1
        self.res2 = res2
        self.time = 0
    def step(self):
        self.time += 1
        #self.spp1.size = self.spp1.size * (1 + self.spp1.efficiency - self.spp1.mortality)
        #self.spp2.size = self.spp2.size * (1 + self.spp2.efficiency - self.spp2.mortality)
        self.spp1.size = self.spp1.size * (1-self.spp1.size/self.spp1.carrying) #HOW TO ADD IN EFFICIENCY AND RESOURCE AVAILABILITY???

        #self.res1.abundance = self.res1.abundance * (1 - (self.spp1.efficiency + self.spp1.efficiency)) + self.res1.reup*(self.res1.maxab-self.res1.abundance)
        #self.res2.abundance = self.res2.abundance * (1 - (self.spp1.efficiency + self.spp1.efficiency)) + self.res2.reup*(self.res2.maxab-self.res2.abundance)
        self.res1.abundance = self.res1.abundance * self.res1.reup * ((self.res1.maxab-self.res1.abundance)/self.res1.maxab)
        self.res2.abundance = self.res2.abundance * self.res2.reup * ((self.res2.maxab-self.res2.abundance)/self.res2.maxab)

class Species:
    def __init__(self, startSize, mortality, efficiency, carrying):
        self.mortality = mortality
        self.size = startSize
        self.efficiency = efficiency
        self.carrying = carrying

class Resource:
    def __init__(self, abundance, replenishRate, maxab):
        self.abundance = abundance
        self.reup = replenishRate
        self.maxab = maxab

def run(spp1start, spp1mort, spp1efficiency, spp2start, spp2mort, spp2efficiency, res1ab, res1reup, res1maxab, res2ab, res2reup, res2maxab, reps):
    spp1 = Species(spp1start, spp1mort, spp1efficiency)
    spp2 = Species(spp2start, spp2mort, spp2efficiency)
    res1 = Resource(res1ab, res1reup, res1maxab)
    res2 = Resource(res2ab, res2reup, res2maxab)
    w = World(spp1, spp2, res1, res2)
    i = 1
    while i <= reps:
        w.step()
        i += 1
    print("\tSpecies 1 abundance = " + str(w.spp1.size) + "\n\tSpecies 2 abundance = " + str(w.spp2.size) + "\n\tResource 1 abundance = " + str(w.res1.abundance) + "\n\tResource 2 abundance = " + str(w.res2.abundance))
