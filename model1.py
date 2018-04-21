import random
import tkinter
random.seed()

def plot(xvals, yvals):
    print(xvals,yvals)
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=400, bg='white')
    c.grid()
    # Create the x-axis.
    c.create_line(50,350,650,350, width=3)
    for i in range(11):
        x = 50 + (i * 58)
        c.create_text(x,355,anchor='n', text='%s'% (i*10) )
    # Create the y-axis.
    c.create_line(50,350,50,50, width=3)
    for i in range(6):
        y = 350 - (i * 60)
        c.create_text(45,y, anchor='e', text='%s'% (1000*i))
    # Plot the points.
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 300*(x-1))
        ypixel = int(350 - 300*y)
        c.create_oval(xpixel-3,ypixel-3,xpixel+3,ypixel+3, width=1, fill='red')
        print('got here')
    root.mainloop()

class World:
    def __init__(self, spp1, spp2, res1, res2):
        self.size = 1000
        self.spp1 = spp1
        self.spp2 = spp2
        self.res1 = res1
        self.res2 = res2
        self.time = 0
    def step(self):
        self.spp1.grow(self.res1, self.res2) #population sizes grow
        self.spp2.grow(self.res1, self.res2)

        if self.spp1.size < 1: #controlling for spp < 1, resource < 0, etc
            self.spp1.size = 0
        if self.spp2.size < 1:
            self.spp2.size = 0
        if self.res1.abundance < 0:
            self.res1.abundance = 0
        if self.res2.abundance < 0:
            self.res2.abundance = 0

        self.time += 1

class Species:
    def __init__(self, startSize, lamb, mortality, carrying, res1lim, res2lim):
        #self.world = 
        self.lamb = float(lamb) #intrinsic growth rate
        self.mortality = float(mortality) #proportion of individuals that will die in each timestep
        self.size = float(startSize) #population size
        self.carrying = float(carrying) #carrying capactiy
        self.res1lim = res1lim
        self.res2lim = res2lim
    def grow(self, res1, res2): #logistic growth equation
        if self.res1lim < res1.conc and self.res2lim < res2.conc:
            self.size = round(self.size * (1 + fi(self) * (self.carrying-self.size)/self.carrying))
            res1.abundance -= self.size
            res2.abundance -= self.size
def fi(spp): #calculate lambda
    rate = spp.lamb - spp.mortality
    return rate

class Resource:
    def __init__(self, abundance, replenishRate):
        #self.world = world
        self.maxab = 500 #max abundance
        self.abundance = abundance
        self.reup = replenishRate #rate at which more resource enters the system
        self.conc = self.abundance/self.world.size
    def getConsumed(self, spp1, spp2): #also logistic growth
        self.abundance = round(self.abundance * (1 + consumption(self, spp1, spp2) * (1-self.abundance/self.maxab)))

def run(reps, spp1start, spp1lamb, spp1mort, spp1carrying, spp1res1lim, spp1res2lim, spp2start, spp2lamb, spp2mort, spp2carrying, spp2res1lim, spp2res2lim, res1ab, res1reup, res2ab, res2reup):
    spp1 = Species(spp1start, spp1lamb, spp1mort, spp1carrying, spp1res1lim, spp1res2lim)
    spp2 = Species(spp2start, spp2lamb, spp2mort, spp2carrying, spp2res1lim, spp2res2lim)
    res1 = Resource(res1ab, res1reup)
    res2 = Resource(res2ab, res2reup)
    w = World(spp1, spp2, res1, res2)
    spp1.world = w
    spp2.world = w
    res1.world = w
    res2.world = w
    #print("Time 1")
    #print("\tSpecies 1 abundance = " + str(w.spp1.size) + "\n\tSpecies 2 abundance = " + str(w.spp2.size) + "\n\tResource 1 abundance = " + str(w.res1.abundance) + "\n\tResource 2 abundance = " + str(w.res2.abundance))
    xvals = []
    yvals = []
    i = 1
    while i <= reps:
        w.step()
        xvals.append(i)
        yvals.append(w.spp1.size)
        i += 1
    return([xvals,yvals])

parameters = {'gens':11, 'spp1start':random.randint(0,1000), 'spp1lamb':random.randint(0,1), 'spp1mort':1, 'spp1carrying':random.randint(0,1000), 'spp1res1lim': 0.2, 'spp1res2lim': 0.3, 'spp2start':random.randint(0,1000), 'spp2lamb':0.7, 'spp2mort':1, 'spp2carrying':random.randint(0,1000), 'spp2res1lim': 0.2, 'spp2res2lim': 0.3, 'res1ab':random.randint(0,1000), 'res1reup':random.randint(0,100), 'res2ab':random.randint(0,1000), 'res2reup':random.randint(0,100)}
running = True
while running == True:
    command = input("Change parameter? ").lower()
    commandwords = command.split()
    if commandwords[0] in parameters and len(commandwords) > 1:
        parameters[commandwords[0]] = int(commandwords[1])
    plot(run(parameters['gens'], parameters['spp1start'], parameters['spp1lamb'], parameters['spp1mort'], parameters['spp1carrying'], parameters['spp1res1lim'], parameters['spp1res2lim'], parameters['spp2start'], parameters['spp2lamb'], parameters['spp2mort'], parameters['spp2carrying'], parameters['spp2res1lim'], parameters['spp2res1lim'], parameters['res1ab'], parameters['res1reup'], parameters['res2ab'], parameters['res2reup']))


