class World:
    def __init__(self, spp1, spp2, res1, res2):
        self.spp1 = spp1
        self.spp2 = spp2
        self.res1 = res1
        self.res2 = res2
        self.time = 0
    def step(self):
        self.time += 1
        self.spp1.grow(self.res1, self.res2) #population sizes grow
        self.spp2.grow(self.res1, self.res2)
        #self.res1.abundance = self.res1.abundance * self.res1.reup * (1-self.res1.abundance)
        #self.res2.abundance = self.res2.abundance * self.res2.reup * (1-self.res2.abundance)
        self.res1.getConsumed(self.spp1, self.spp2) #resources get consumed
        self.res2.getConsumed(self.spp1, self.spp2)

        if self.spp1.size < 1: #controlling for spp < 1, resource < 0, etc
            self.spp1.size = 0
        if self.spp2.size < 1:
            self.spp2.size = 0
        if self.res1.abundance < 0:
            self.res1.abundance = 0
        elif self.res1.abundance > 1:
            self.res1.abundance = 1
        if self.res2.abundance < 0:
            self.res2.abundance = 0
        elif self.res2.abundance > 1:
            self.res2.abundance = 1

class Species:
    def __init__(self, startSize, lamb, mortality, carrying):
        self.lamb = float(lamb) #intrinsic growth rate
        self.mortality = float(mortality) #proportion of individuals that will die in each timestep
        self.size = float(startSize) #population size
        self.carrying = float(carrying) #carrying capactiy
    def grow(self, res1, res2): #logistic growth equation
        self.size = round(self.size * (1 + fi(self, res1, res2) * (self.carrying-self.size)/self.carrying))
def fi(spp, res1, res2): #calculate lambda
    rate = (spp.lamb - spp.mortality) * res1.abundance * res2.abundance
    return rate

class Resource:
    def __init__(self, abundance, replenishRate):
        self.maxab = 500 #max abundance
        self.abundance = abundance #0 to 1, to represent the proportion of individuals of a species that has access to the resource
        self.reup = replenishRate #rate at which more resource enters the system
    def getConsumed(self, spp1, spp2): #also logistic growth
        self.abundance = round(self.abundance * (1 + consumption(self, spp1, spp2) * (1-self.abundance/self.maxab)))
def consumption(res, spp1, spp2): #like lambda but for resources
    rate = res.reup - (spp1.size * 2 + spp2.size * 3) #arbitrary numbers
    return rate

def run(reps, spp1start, spp1lamb, spp1mort, spp1carrying, spp2start, spp2lamb, spp2mort, spp2carrying, res1ab, res1reup, res2ab, res2reup):
    #spp1start = float(input("Species 1 starting density? "))
    #spp1mort = float(input("Species 1 mortality? "))
    #spp1efficiency = float(input("Species 1 efficiency? "))
    #spp1carrying = float(input("Species 1 carrying capacity? "))
    #spp2start = float(input("Species 2 starting density? "))
    #spp2mort = float(input("Species 2 mortality? "))
    #spp2efficiency = float(input("Species 2 efficiency? "))
    #spp2carrying = float(input("Species 2 carrying capacity? "))
    #res1ab = float(input("Resource 1 abundance? "))
    #res1reup = float(input("Resource 1 replenishment rate? "))
    #res2ab = float(input("Resource 2 abundance? "))
    #res2reup = float(input("Resource 2 replenishment rate? "))
    spp1 = Species(spp1start, spp1lamb, spp1mort, spp1carrying)
    spp2 = Species(spp2start, spp2lamb, spp2mort, spp2carrying)
    res1 = Resource(res1ab, res1reup)
    res2 = Resource(res2ab, res2reup)
    w = World(spp1, spp2, res1, res2)
    print("Time 1")
    print("\tSpecies 1 abundance = " + str(w.spp1.size) + "\n\tSpecies 2 abundance = " + str(w.spp2.size) + "\n\tResource 1 abundance = " + str(w.res1.abundance) + "\n\tResource 2 abundance = " + str(w.res2.abundance))
    i = 1
    while i <= reps:
        w.step()
        i += 1
        print("Time " + str(i))
        print("\tSpecies 1 abundance = " + str(w.spp1.size) + "\n\tSpecies 2 abundance = " + str(w.spp2.size) + "\n\tResource 1 abundance = " + str(w.res1.abundance) + "\n\tResource 2 abundance = " + str(w.res2.abundance))
