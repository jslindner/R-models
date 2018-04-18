class World:
    def __init__(self, spp1, spp2, res1, res2):
        self.spp1 = spp1
        self.spp2 = spp2
        self.res1 = res1
        self.res2 = res2
        self.time = 0
    def step(self):
        self.time += 1
        self.spp1.size = self.spp1.size * (1-self.spp1.size/self.spp1.carrying) * self.res1.abundance * self.res2.abundance
        self.spp2.size = self.spp2.size * (1-self.spp2.size/self.spp2.carrying) * self.res1.abundance * self.res2.abundance
        self.res1.abundance = self.res1.abundance * self.res1.reup * ((self.res1.maxab-self.res1.abundance)/self.res1.maxab)
        self.res2.abundance = self.res2.abundance * self.res2.reup * ((self.res2.maxab-self.res2.abundance)/self.res2.maxab)
        if self.res1.abundance < 0:
            self.res1.abundance = 0
        if self.res2.abundance < 0:
            self.res2.abundance = 0

class Species:
    def __init__(self, startSize, mortality, efficiency, carrying):
        self.mortality = mortality
        self.size = startSize
        self.efficiency = efficiency
        self.carrying = carrying

class Resource:
    def __init__(self, abundance, replenishRate, maxab):
        self.abundance = abundance #0 to 1, to represent the proportion of individuals of a species that has access to the resource
        self.reup = replenishRate
        self.maxab = maxab

def run(reps):
    spp1start = float(input("Species 1 starting density? "))
    spp1mort = float(input("Species 1 mortality? "))
    spp1efficiency = float(input("Species 1 efficiency? "))
    spp1carrying = float(input("Species 1 carrying capacity? "))
    spp2start = float(input("Species 2 starting density? "))
    spp2mort = float(input("Species 2 mortality? "))
    spp2efficiency = float(input("Species 2 efficiency? "))
    spp2carrying = float(input("Species 2 carrying capacity? "))
    res1ab = float(input("Resource 1 abundance? "))
    res1reup = float(input("Resource 1 replenishment rate? "))
    res1maxab = float(input("Resource 1 maximum abundance? "))
    res2ab = float(input("Resource 2 abundance? "))
    res2reup = float(input("Resource 2 replenishment rate? "))
    res2maxab = float(input("Resource 2 maximum abundance? "))
    spp1 = Species(spp1start, spp1mort, spp1efficiency, spp1carrying)
    spp2 = Species(spp2start, spp2mort, spp2efficiency, spp2carrying)
    res1 = Resource(res1ab, res1reup, res1maxab)
    res2 = Resource(res2ab, res2reup, res2maxab)
    w = World(spp1, spp2, res1, res2)
    i = 1
    while i <= reps:
        w.step()
        i += 1
        print("Step " + str(i))
        print("\tSpecies 1 abundance = " + str(w.spp1.size) + "\n\tSpecies 2 abundance = " + str(w.spp2.size) + "\n\tResource 1 abundance = " + str(w.res1.abundance) + "\n\tResource 2 abundance = " + str(w.res2.abundance))














