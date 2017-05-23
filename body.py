from tkinter import *
import random
import math

global canvas, root

circs = []
generation = []
nextGeneration = []
fitrange = []

crossFactor = 0.7
muteFactor = 0.001
genSize = 500
total = 0
curBest = 0

canvas = Canvas(root, width=800, height=600)

def init_module(a):
    global root, canvas
    root = a
    canvas = Canvas(root, width=800, height=600)

def clearMap():
    canvas.delete(curBest)
'''
    Individual
'''

class Individual:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def valid(self):
        min_dist = min(min(self.x, 800 - self.x), min(self.y, 600 - self.y))
        for i in range(len(circs)):
            dist = int(math.sqrt((self.x - circs[i].x)*(self.x - circs[i].x) + (self.y - circs[i].y)*(self.y - circs[i].y)))
            min_dist = min(min_dist, dist)
        return min_dist >= 0

    def encode(self):
        return to_bin(self.x)+to_bin(self.y)

    def fitness(self):
        return Circunference(self.x, self.y, 0).fitness()

'''
    Circunference
'''

class Circunference:
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad

    def dist(self, circ):
        return int(math.sqrt((self.x - circ.x)*(self.x - circ.x) + (self.y - circ.y)*(self.y - circ.y)) -
                   self.rad - circ.rad)

    def fitness(self):
        global circs
        val = min(min(self.x, 800 - self.x), min(self.y, 600 - self.y))
        for i in range(len(circs)):
            val = min(val, self.dist(circs[i]))
        return val

    def fit(self):
        return self.x + self.rad <= 800 and self.x - self.rad >= 0 and self.y - self.rad <= 600 and self.y + self.rad >= 0

    def plot(self, t):
        global canvas
        a = self.x - self.rad
        b = self.y - self.rad
        c = self.x + self.rad
        d = self.y + self.rad
        if (t == 1):
            canvas.create_oval(a, b, c, d, fill = "white")
        else:
            global curBest
            curBest = canvas.create_oval(a, b, c, d, fill = "red")

'''
    Util
'''

def to_bin(x):
    bina = ""
    while (x > 0):
        bina += str(x % 2)
        x = int(x/2)

    while (len(bina) < 10):
        bina += "0"

    return bina[::-1]

def to_int(s):
    val = 0
    s = s[::-1]
    for i in range(len(s)):
        if (s[i] == '1'):
            val += (1<<i)
    return val

def decode(s):
    lhs = ""
    rhs = ""
    for i in range(len(s)):
        if (i < int(len(s)/2)):
            lhs += s[i]
        else:
            rhs += s[i]
    return Individual(to_int(lhs), to_int(rhs))

def update():
    global total, fitrange, generation
    total = 0
    for i in range(len(generation)):
        fitrange.append(generation[i].fitness())
        total += generation[i].fitness();

def init_circles():
    global circs
    for i in range(70):
        x = random.randint(40, 759)
        y = random.randint(40, 559)
        rad = random.randint(20, 40)
        aux = Circunference(x, y, rad)
        if (aux.fitness() >= 0 and aux.fit()):
            circs.append(aux)

    for i in range(len(circs)):
        circs[i].plot(1)

def genFirstGeneration():
    global generation
    while (len(generation) < genSize):
        x = random.randint(0, 799)
        y = random.randint(0, 599)
        ind = Individual(x, y)
        if (ind.valid()):
            generation.append(ind)
    update()

def getBestIndividual():
    global generation
    best = Circunference(0, 0, 0)
    for i in range(len(generation)):
        c = Circunference(generation[i].x, generation[i].y, 0)
        f = c.fitness()
        c = Circunference(generation[i].x, generation[i].y, f)
        if (c.fitness() > best.fitness()):
            best = c
    best.plot(0)

def comp(a):
    return a.fitness()

def getNextGeneration():
    nextGeneration = []
    
    global total, generation, fitrange
    global muteFactor, crossFactor

    media = 0
    for i in range(len(generation)):
        media += generation[i].fitness()
    media /= len(generation)

    generation = sorted(generation, key=comp)
    val = genSize - 50
    best = generation[val:]

    del fitrange[:]
    total = 0
    for i in range(len(best)):
        total += best[i].fitness()
        fitrange.append(best[i].fitness())

    sz = len(best)
    
    while (len(nextGeneration) < genSize):
        ind1 = 0
        ind2 = 0

        ix = 0
        while (True):
            r = random.random()
            f = fitrange[ix] / total
            if (r <= f):
                ind1 = best[ix]
                break;
            ix = (ix + 1) % sz

        ix = 0
        while (True):
            r = random.random()
            f = fitrange[ix] / total
            if (r <= f):
                ind2 = best[ix]
                break;
            ix = (ix + 1) % sz

        r = random.random()
        son = Individual(r * ind1.x + (1 - r) * ind2.x, (1.0 - r) * ind1.y + r * ind2.y)
        
        if (son.valid()):
            nextGeneration.append(son)
            
        '''
        s = ind1.encode()
        w = ind2.encode()

        for i in range(len(s)):
            r = random.random()
            if (r < crossFactor):
                ss = s[:i]+w[i:len(w)]
                ww = w[:i]+s[i:len(s)]
                s = ss
                w = ww

        for i in range(len(s)):
            r = random.random()
            if (r < muteFactor):
                if (s[i] == '0'):
                    s = list(s)
                    s[i] = '1'
                    s = "".join(s)
                else:
                    s = list(s)
                    s[i] = '0'
                    s = "".join(s)

        for i in range(len(w)):
            r = random.random()
            if (r < muteFactor):
                if (w[i] == '0'):
                    w = list(w)
                    w[i] = '1'
                    w = "".join(w)
                else:
                    w = list(w)
                    w[i] = '0'
                    w = "".join(w)

        s = decode(s)
        w = decode(w)
        if (s.valid() and s.fitness() > media):
            nextGeneration.append(s)

        if (w.valid() and w.fitness() > media):
            nextGeneration.append(w)
        '''
    del generation[:]
    for i in range(len(nextGeneration)):
        generation.append(nextGeneration[i])

    del nextGeneration[:]
    update()

canvas.pack()
