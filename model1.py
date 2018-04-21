import random
import tkinter
random.seed()

def plot(xvals, yvals):
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=600, bg='white')
    c.grid()
    # Create the x-axis.
    c.create_line(50,550,650,550, width=3)
    for i in range(11):
        x = 50 + (i * 60)
        c.create_text(x,555,anchor='n', text='%s'% i)
    # Create the y-axis.
    c.create_line(50,550,50,50, width=3)
    for i in range(11):
        y = 550 - (i * 50)
        c.create_text(45,y, anchor='e', text='%s'% (200*i))
    # Plot the points.
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 60 * x)
        ypixel = int(550 - y/4)
        c.create_oval(xpixel-3,ypixel-3,xpixel+3,ypixel+3, width=1, fill='red')
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
        self.spp1.grow(self.res1, self.res2) #populations grow AND resources get consumed
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
        res1.abundance = 1 + res1.reup * ((res1.maxab-res1.abundance)/res1.maxab)
        res2.abundance = 1 + res2.reup * ((res2.maxab-res2.abundance)/res2.maxab)
def fi(spp): #calculate lambda
    rate = spp.lamb - spp.mortality
    return rate

class Resource:
    def __init__(self, abundance, replenishRate):
        self.maxab = 1000 #max abundance
        self.abundance = abundance
        self.reup = replenishRate #rate at which more resource enters the system
        self.conc = self.abundance/1000
    
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
    xvals = []
    yvals = []
    res1x = []
    res1y = []
    i = 1
    while i <= reps:
        w.step()
        xvals.append(i)
        yvals.append(w.spp1.size)
        #res1x.append(i)
        #res1y.append(w.res1.abundance)
        i += 1
    #print(xvals,yvals)
    return [xvals, yvals]

parameters = {'gens':10, 'spp1start':random.randint(0,1000), 'spp1lamb':random.randint(0,1), 'spp1mort':1, 'spp1carrying':random.randint(0,1000), 'spp1res1lim': 0.2, 'spp1res2lim': 0.3, 'spp2start':random.randint(0,1000), 'spp2lamb':0.7, 'spp2mort':1, 'spp2carrying':random.randint(0,1000), 'spp2res1lim': 0.2, 'spp2res2lim': 0.3, 'res1ab':random.randint(0,1000), 'res1reup':random.randint(0,100), 'res2ab':random.randint(0,1000), 'res2reup':random.randint(0,100)}
running = True
while running == True:
    command = input("Change parameter? ").lower()
    commandwords = command.split()
    if commandwords[0] in parameters and len(commandwords) > 1:
        parameters[commandwords[0]] = int(commandwords[1])
    vals = run(parameters['gens'], parameters['spp1start'], parameters['spp1lamb'], parameters['spp1mort'], parameters['spp1carrying'], parameters['spp1res1lim'], parameters['spp1res2lim'], parameters['spp2start'], parameters['spp2lamb'], parameters['spp2mort'], parameters['spp2carrying'], parameters['spp2res1lim'], parameters['spp2res1lim'], parameters['res1ab'], parameters['res1reup'], parameters['res2ab'], parameters['res2reup'])
    plot(vals[0],vals[1])


