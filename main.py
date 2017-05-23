from tkinter import *
from threading import Thread
import random
import math

global canvas, root

root = Tk()
root.title("Generation = 0")
canvas = Canvas(root, height = 600, width = 800)

circs = []
generation = []
nextGeneration = []
fitrange = []

crossFactor = 0.7
muteFactor = 0.001
genSize = 100
total = 0
curBest = 0

bestAns = 0
curAns = 0

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

def init_circles():
    global circs
    for i in range(50):
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

def getBestIndividual():
    global generation, curAns
    best = 0
    bestInd = generation[0]
    for i in range(len(generation)):
        c = generation[i]
        if (c.fitness() > best):
            best = c.fitness()
            bestInd = c

    curAns = int(best)
    Circunference(bestInd.x, bestInd.y, bestInd.fitness()).plot(0)

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
    best = generation[:]

    del fitrange[:]
    total = 0
    
    for i in range(len(best)):
        total += best[i].fitness()
        fitrange.append(best[i].fitness())

    while (len(nextGeneration) < genSize):
        sz = min(len(best), len(fitrange))
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
        if (s.valid() and s.fitness() >= media):
            nextGeneration.append(s)

        if (w.valid() and w.fitness() >= media):
            nextGeneration.append(w)
        
    del generation[:]
    for i in range(len(nextGeneration)):
        generation.append(nextGeneration[i])

    del nextGeneration[:]

def getGlobalBest():
    global bestAns
    best = 0
    for i in range(800):
        for j in range(600):
            best = max(best, Individual(i, j).fitness())
    bestAns = best

global counter
counter = 0

class Th(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global canvas, generation, counter, bestAns, curAns
        canvas.delete(curBest)
        getNextGeneration()
        getBestIndividual()
        counter += 1
        root.title("Generation = "+str(counter)+" Best Radius = "+str(bestAns)+" Current Radius = "+str(curAns))
        canvas.pack()

init_circles()
genFirstGeneration()
getBestIndividual()
getGlobalBest()

global going

def start():
    global going
    going = Th()
    going.start()
    
def stop():
    global going
    going.paused = True

play = Button(canvas, text = "Next Generation", command = start, anchor = W)
play_window = canvas.create_window(10, 10, anchor = NW, window = play)

canvas.pack()
root.mainloop()
