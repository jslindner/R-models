import random
import tkinter
random.seed()

def plot_time(to_plot):
    spp1xs = to_plot[0]
    spp1ys = to_plot[1]
    spp2ys = to_plot[2]
    res1ys = to_plot[3]
    res2ys = to_plot[4]
    gens = to_plot[5]
    space = round(600/gens)
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=600, bg='white')
    c.grid()
    # Create the x-axis.
    c.create_line(50,550,650,550, width=3)
    for i in range(gens+1):
        x = 50 + (i * space)
        c.create_text(x,555,anchor='n', text='%s'% i)
    # Create the y-axis.
    c.create_line(50,550,50,50, width=3)
    for i in range(11):
        y = 550 - (i * 50)
        c.create_text(45,y, anchor='e', text='%s'% (200*i))
    c.create_text(400,200,text='spp1 red\nspp2 green\nres1 blue\nres2 yellow')
    # Plot the points.
    for i in range(gens):
        spp1x, spp1y = spp1xs[i], spp1ys[i]
        spp1xpixel = int(50 + space * spp1x)
        spp1ypixel = int(550 - spp1y/4)
        c.create_line(spp1xpixel, spp1ypixel, int(50 + space * spp1xs[i-1]), int(550 - spp1ys[i-1]/4), fill = 'red', width = 2)
        c.create_oval(spp1xpixel-3,spp1ypixel-3,spp1xpixel+3,spp1ypixel+3, width=1, fill='red')
        spp2ypixel = int(550 - spp2ys[i]/4)
        c.create_line(spp1xpixel, spp2ypixel, int(50 + space * spp1xs[i-1]), int(550 - spp2ys[i-1]/4), fill = 'green', width = 2)
        c.create_oval(spp1xpixel-3,spp2ypixel-3,spp1xpixel+3,spp2ypixel+3, width=1, fill='green')
        res1ypixel = int(550 - res1ys[i]/4)
        c.create_line(spp1xpixel, res1ypixel, int(50 + space * spp1xs[i-1]), int(550 - res1ys[i-1]/4), fill = 'blue', width = 2)
        c.create_rectangle(spp1xpixel-3,res1ypixel-3,spp1xpixel+3,res1ypixel+3, width=1, fill='blue')
        res2ypixel = int(550 - res2ys[i]/4)
        c.create_line(spp1xpixel, res2ypixel, int(50 + space * spp1xs[i-1]), int(550 - res2ys[i-1]/4), fill = 'yellow', width = 2)
        c.create_rectangle(spp1xpixel-3,res2ypixel-3,spp1xpixel+3,res2ypixel+3, width=1, fill='yellow')
    #root.mainloop()

class World:
    def __init__(self, spp1, spp2, res1, res2):
        self.spp1 = spp1
        self.spp2 = spp2
        self.res1 = res1
        self.res2 = res2
    def step(self):
        self.spp1.grow()
        self.spp2.grow()
        self.res1.ab = self.res1.ab - (self.spp1.size + self.spp2.size)
        self.res2.ab = self.res2.ab - (self.spp1.size + self.spp2.size)
        if self.spp1.size < 0:
            self.spp1.size = 0
        if self.spp2.size < 0:
            self.spp2.size = 0
        if self.res1.ab < 0:
            self.res1.ab = 0
        if self.res2.ab < 0:
            self.res2.ab = 0
        self.res1.grow()
        self.res2.grow()
        return [self.spp1.size, self.spp2.size, self.res1.ab, self.res2.ab]

class Species():
    def __init__(self, size, r, m, k, res1lim, res2lim):
        self.size = size
        self.r = r
        self.m = m
        self.k = k
        self.res1lim = res1lim
        self.res2lim = res2lim
    def grow(self):
        self.size = self.size + self.size * (self.r - self.m) * ((self.k-self.size)/self.k) * (self.world.res1.conc - self.res1lim) * (self.world.res2.conc - self.res2lim)
        if self.size > self.k:
            self.size = self.k

class Resource():
    def __init__(self, ab, reup, maxab):
        self.ab = ab
        self.reup = reup
        self.maxab = maxab
        self.conc = self.ab/100
    def grow(self):
        self.ab = self.ab + self.ab * self.reup * ((self.maxab - self.ab)/self.maxab)
        self.conc = self.ab/100
        if self.ab > self.maxab:
            self.ab = self.maxab

def test_nums(spp1s, spp1r, spp1m, spp1k, spp1res1lim, spp1res2lim, spp2s, spp2r, spp2m, spp2k, spp2res1lim, spp2res2lim, res1ab, res1reup, res1max, res2ab, res2reup, res2max, reps):
    spp1 = Species(spp1s, spp1r, spp1m, spp1k, spp1res1lim, spp1res2lim)
    spp2 = Species(spp2s, spp2r, spp2m, spp2k, spp2res1lim, spp2res2lim)
    res1 = Resource(res1ab, res1reup, res1max)
    res2 = Resource(res2ab, res2reup, res2max)
    w = World(spp1, spp2, res1, res2)
    spp1.world = w
    spp2.world = w
    res1.world = w
    res2.world = w
    spp1xs = []
    spp1ys = []
    spp2ys = []
    res1ys = []
    res2ys = []
    spp1xs.append(1)
    spp1ys.append(spp1s)
    spp2ys.append(spp2s)
    res1ys.append(res1ab)
    res2ys.append(res2ab)
    i = 2
    while i <= reps:
        vals = w.step()
        spp1xs.append(i)
        spp1ys.append(vals[0])
        spp2ys.append(vals[1])
        res1ys.append(vals[2])
        res2ys.append(vals[3])
        i += 1
    to_plot = [spp1xs,spp1ys,spp2ys,res1ys,res2ys,reps]
    return to_plot
def test_time(to_plot):
    plot_time(to_plot)

def test_rstar(to_plot):
    plot_rstar(to_plot)
def plot_rstar(to_plot):
    spp1xs = [to_plot[0]]
    spp1ys = [to_plot[1]]
    spp2ys = [to_plot[2]]
    res1ys = [to_plot[3]]
    res2ys = [to_plot[4]]
    gens = to_plot[5]
    space = round(600/gens)
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=600, bg='white')
    c.grid()
    # Create the x-axis.
    c.create_line(50,550,650,550, width=3)
    c.create_text(400,575,text = 'Resource 1 concentration')
    c.create_text(50,560,text = '0')
    c.create_text(650,560,text = '1')
    # Create the y-axis.
    c.create_line(50,550,50,50, width=3)
    c.create_text(10,100,text="\n".join("Resource 2 concentration"), anchor="nw")
    c.create_text(400,200,text='spp1 red\nspp2 green\nres1 blue\nres2 yellow')
    c.create_text(40,550,text = '0')
    c.create_text(40,50,text = '1')
    #Create ZGI 1
    c.create_line(100,50,100,400, width = 3)
    c.create_line(100,400,600,400, width = 3)
    #Create ZGI 1
    # c.create_line(200,50,200,500, width = 3)
    # c.create_line(200,500,600,500, width = 3)
    spp1xstart,spp1ystart = spp1xs[0],spp1ys[0]
    spp1xdone,spp1ydone = spp1xs[len(spp1xs)-1],spp1ys[len(spp1xs)-1]
    # spp2xstart,spp2ystart = spp1xs[0],spp2ys[0]
    # spp2xdone,spp2ydone = spp1xs[len(spp1xs)-1],spp2ys[len(spp1xs)-1]
    c.create_line(spp1xstart,spp1ystart,spp1xdone,spp1ydone, width = 3, fill = 'red')







