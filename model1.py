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
        self.spp1 = spp1
        self.spp2 = spp2
        self.res1 = res1
        self.res2 = res2
        self.time = 0
    def step(self):
        self.time += 1
        self.spp1.grow(self.res1, self.res2) #population sizes grow
        self.spp2.grow(self.res1, self.res2)
        self.res1.getConsumed(self.spp1, self.spp2) #resources get consumed
        self.res2.getConsumed(self.spp1, self.spp2)

        if self.spp1.size < 1: #controlling for spp < 1, resource < 0, etc
            self.spp1.size = 0
        if self.spp2.size < 1:
            self.spp2.size = 0
        if self.res1.abundance < 0:
            self.res1.abundance = 0
        if self.res2.abundance < 0:
            self.res2.abundance = 0
        
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
    spp1 = Species(spp1start, spp1lamb, spp1mort, spp1carrying)
    spp2 = Species(spp2start, spp2lamb, spp2mort, spp2carrying)
    res1 = Resource(res1ab, res1reup)
    res2 = Resource(res2ab, res2reup)
    w = World(spp1, spp2, res1, res2)
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

parameters = {'gens':11, 'spp1start':random.randint(0,1000), 'spp1lamb':random.randint(0,1), 'spp1mort':1, 'spp1carrying':random.randint(0,1000), 'spp2start':random.randint(0,1000), 'spp2lamb':0.7, 'spp2mort':1, 'spp2carrying':random.randint(0,1000), 'res1ab':random.randint(0,1000), 'res1reup':random.randint(0,100), 'res2ab':random.randint(0,1000), 'res2reup':random.randint(0,100)}
running = True
while running == True:
    command = input("Change parameter? ").lower()
    commandwords = command.split()
    if commandwords[0] in parameters and len(commandwords) > 1:
        parameters[commandwords[0]] = int(commandwords[1])
    plot(run(parameters['gens'], parameters['spp1start'], parameters['spp1lamb'], parameters['spp1mort'], parameters['spp1carrying'], parameters['spp2start'], parameters['spp2lamb'], parameters['spp2mort'], parameters['spp2carrying'], parameters['res1ab'], parameters['res1reup'], parameters['res2ab'], parameters['res2reup']))


