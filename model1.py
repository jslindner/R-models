import random
import tkinter
random.seed()

def plot(spp1xs, spp1ys, spp2ys, res1ys, res2ys, gens):
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=600, bg='white')
    c.grid()
    # Create the x-axis.
    c.create_line(50,550,650,550, width=3)
    for i in range(1,11):
        x = 50 + (i * 60)
        p = round(gens/i)
        c.create_text(x,555,anchor='n', text='%s'% p)
    # Create the y-axis.
    c.create_line(50,550,50,50, width=3)
    for i in range(11):
        y = 550 - (i * 50)
        c.create_text(45,y, anchor='e', text='%s'% (200*i))
    c.create_text(400,200,text='spp1 red\nspp2 green\nres1 blue\nres2 yellow')
    # Plot the points.
    for i in range(len(spp1xs)):
        spp1x, spp1y = spp1xs[i], spp1ys[i]
        spp1xpixel = int(50 + 60 * spp1x)
        spp1ypixel = int(550 - spp1y/4)
        c.create_line(spp1xpixel, spp1ypixel, int(50 + 60 * spp1xs[i-1]), int(550 - spp1ys[i-1]/4), fill = 'red', width = 2)
        c.create_oval(spp1xpixel-3,spp1ypixel-3,spp1xpixel+3,spp1ypixel+3, width=1, fill='red')
        spp2ypixel = int(550 - spp2ys[i]/4)
        c.create_line(spp1xpixel, spp2ypixel, int(50 + 60 * spp1xs[i-1]), int(550 - spp2ys[i-1]/4), fill = 'green', width = 2)
        c.create_oval(spp1xpixel-3,spp2ypixel-3,spp1xpixel+3,spp2ypixel+3, width=1, fill='green')
        res1ypixel = int(550 - res1ys[i]/4)
        c.create_line(spp1xpixel, res1ypixel, int(50 + 60 * spp1xs[i-1]), int(550 - res1ys[i-1]/4), fill = 'blue', width = 2)
        c.create_rectangle(spp1xpixel-3,res1ypixel-3,spp1xpixel+3,res1ypixel+3, width=1, fill='blue')
        res2ypixel = int(550 - res2ys[i]/4)
        c.create_line(spp1xpixel, res2ypixel, int(50 + 60 * spp1xs[i-1]), int(550 - res2ys[i-1]/4), fill = 'yellow', width = 2)
        c.create_rectangle(spp1xpixel-3,res2ypixel-3,spp1xpixel+3,res2ypixel+3, width=1, fill='yellow')
    #root.mainloop()
class World:
    def __init__(self, spp1, spp2, res1, res2):
        self.size = 1000
        self.spp1 = spp1
        self.spp2 = spp2
        self.res1 = res1
        self.res2 = res2
        self.time = 0
    def step(self):
        delta1 = self.spp1.grow(self.res1, self.res2) #populations grow AND resources get consumed
        delta2 = self.spp2.grow(self.res1, self.res2)
        self.res1.grow(self.spp1, self.spp2, delta1, delta2)
        self.res2.grow(self.spp1, self.spp2, delta1, delta2)
        

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
        old = self.size
        self.size = self.size + self.size * (self.lamb - self.mortality) * ((self.carrying-self.size)/self.carrying)*(res1.conc - self.res1lim)*(res2.conc - self.res2lim)
        delta = self.size - old
        return delta

class Resource:
    def __init__(self, abundance, replenishRate):
        self.maxab = 1000 #max abundance
        self.abundance = abundance
        self.reup = replenishRate #rate at which more resource enters the system
        self.conc = self.abundance/1000 
    def grow(self, spp1, spp2, delta1, delta2):
        self.abundance = self.abundance - spp1.size - spp2.size - 2*delta1 - 2*delta2
        self.abundance = self.abundance + self.abundance * self.reup * ((self.maxab-self.abundance)/self.maxab)

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
    spp1x = []
    spp1y = []
    spp2y = []
    res1y = []
    res2y = []
    i = 1
    while i <= reps:
        #print('size1 = ' + str(spp1.size))
        #print('size2 = ' + str(spp2.size))
        #print('res1conc = ' + str(res1.conc))
        #print('res2conc = ' + str(res2.conc))
        spp1x.append(i)
        spp1y.append(w.spp1.size)
        spp2y.append(w.spp2.size)
        res1y.append(w.res1.abundance)
        res2y.append(w.res2.abundance)
        w.step()
        i += 1
    return [spp1x, spp1y, spp2y, res1y, res2y]

parameters = {'gens':30, 'spp1start':20, 'spp1lamb':0.4, 'spp1mort':0.2, 'spp1carrying':500, 'spp1res1lim': 0.2, 'spp1res2lim': 0.3, 'spp2start':100, 'spp2lamb':0.3, 'spp2mort':0.2, 'spp2carrying':300, 'spp2res1lim': 0.2, 'spp2res2lim': 0.3, 'res1ab':400, 'res1reup':20, 'res2ab':900, 'res2reup':50}
running = True
while running == True:
    vals = run(parameters['gens'], parameters['spp1start'], parameters['spp1lamb'], parameters['spp1mort'], parameters['spp1carrying'], parameters['spp1res1lim'], parameters['spp1res2lim'], parameters['spp2start'], parameters['spp2lamb'], parameters['spp2mort'], parameters['spp2carrying'], parameters['spp2res1lim'], parameters['spp2res1lim'], parameters['res1ab'], parameters['res1reup'], parameters['res2ab'], parameters['res2reup'])
    plot(vals[0],vals[1],vals[2],vals[3],vals[4],parameters['gens'])
    command = input("Change parameter? ").lower()
    commandwords = command.split()
    while commandwords[0] not in parameters:
        command = input("Change parameter? ").lower()
        commandwords = command.split()
    if commandwords[0] in parameters and len(commandwords) > 1:
        parameters[commandwords[0]] = float(commandwords[1])


